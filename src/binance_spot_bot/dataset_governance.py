from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field, replace
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

from .redaction import redact_payload
from .types import Candle, FeatureRow, LabelRow


@dataclass(frozen=True)
class FeatureSchema:
    feature_names: list[str]
    feature_types: dict[str, str]
    normalisation: str
    lookback_window: int
    generator_version: str = "features-v1"

    @property
    def schema_hash(self) -> str:
        return feature_schema_hash(self.feature_names, self.feature_types, self.normalisation, self.lookback_window, self.generator_version)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["schema_hash"] = self.schema_hash
        return payload


@dataclass(frozen=True)
class DatasetManifest:
    dataset_id: str
    created_at_ms: int
    source: str
    symbols: list[str]
    interval: str
    raw_data_range: dict[str, int | None]
    feature_range: dict[str, int | None]
    label_range: dict[str, int | None]
    train_range: dict[str, int | None]
    validation_range: dict[str, int | None]
    test_range: dict[str, int | None]
    feature_set_version: str
    feature_schema_hash: str
    label_name: str
    label_horizon: int
    fee_bps: str
    slippage_bps: str
    spread_bps: str
    data_quality_summary: dict[str, Any]
    row_count: int
    gap_count: int
    duplicate_count: int
    checksum: str = ""

    def with_checksum(self) -> "DatasetManifest":
        return replace(self, checksum=manifest_checksum(asdict(replace(self, checksum=""))))

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.with_checksum().to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: Path) -> "DatasetManifest":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(**payload)


@dataclass(frozen=True)
class LeakageIssue:
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class LeakageReport:
    status: str
    issues: list[LeakageIssue] = field(default_factory=list)
    gap_count: int = 0
    duplicate_count: int = 0

    @property
    def passed(self) -> bool:
        return self.status == "pass"

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "passed": self.passed,
            "issues": [issue.to_dict() for issue in self.issues],
            "gap_count": self.gap_count,
            "duplicate_count": self.duplicate_count,
        }


def feature_schema_from_rows(rows: Iterable[FeatureRow], *, lookback_window: int, generator_version: str = "features-v1") -> FeatureSchema:
    first = next(iter(rows), None)
    names = sorted(first.values.keys()) if first else []
    return FeatureSchema(
        feature_names=names,
        feature_types={name: "float" for name in names},
        normalisation="raw",
        lookback_window=lookback_window,
        generator_version=generator_version,
    )


def feature_schema_hash(
    feature_names: list[str],
    feature_types: dict[str, str] | None = None,
    normalisation: str = "raw",
    lookback_window: int = 0,
    generator_version: str = "features-v1",
) -> str:
    payload = {
        "feature_names": list(feature_names),
        "feature_types": feature_types or {name: "float" for name in feature_names},
        "normalisation": normalisation,
        "lookback_window": lookback_window,
        "generator_version": generator_version,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def validate_feature_schema(rows: Iterable[FeatureRow], expected_hash: str, *, lookback_window: int, generator_version: str = "features-v1") -> None:
    schema = feature_schema_from_rows(rows, lookback_window=lookback_window, generator_version=generator_version)
    if schema.schema_hash != expected_hash:
        raise ValueError(f"feature schema mismatch: expected {expected_hash}, got {schema.schema_hash}")


def build_dataset_manifest(
    *,
    dataset_id: str,
    source: str,
    symbol: str,
    interval: str,
    candles: list[Candle],
    features: list[FeatureRow],
    labels: list[LabelRow],
    train_rows: list[FeatureRow],
    validation_rows: list[FeatureRow],
    test_rows: list[FeatureRow],
    lookback_window: int,
    label_horizon: int,
    fee_bps: Decimal = Decimal("10"),
    slippage_bps: Decimal = Decimal("5"),
    spread_bps: Decimal = Decimal("0"),
) -> DatasetManifest:
    leakage = leakage_guard(
        features,
        labels,
        train_rows=train_rows,
        validation_rows=validation_rows,
        test_rows=test_rows,
        label_horizon=label_horizon,
    )
    schema = feature_schema_from_rows(features, lookback_window=lookback_window)
    return DatasetManifest(
        dataset_id=dataset_id,
        created_at_ms=int(time.time() * 1000),
        source=source,
        symbols=[symbol],
        interval=interval,
        raw_data_range=_range_from_candles(candles),
        feature_range=_range_from_rows(features),
        label_range=_range_from_labels(labels),
        train_range=_range_from_rows(train_rows),
        validation_range=_range_from_rows(validation_rows),
        test_range=_range_from_rows(test_rows),
        feature_set_version=schema.generator_version,
        feature_schema_hash=schema.schema_hash,
        label_name="future_return_up",
        label_horizon=label_horizon,
        fee_bps=str(fee_bps),
        slippage_bps=str(slippage_bps),
        spread_bps=str(spread_bps),
        data_quality_summary=leakage.to_dict(),
        row_count=len(features),
        gap_count=leakage.gap_count,
        duplicate_count=leakage.duplicate_count,
    ).with_checksum()


def leakage_guard(
    features: list[FeatureRow],
    labels: list[LabelRow],
    *,
    train_rows: list[FeatureRow],
    validation_rows: list[FeatureRow],
    test_rows: list[FeatureRow],
    label_horizon: int,
    embargo: int | None = None,
) -> LeakageReport:
    issues: list[LeakageIssue] = []
    embargo = label_horizon if embargo is None else embargo
    feature_ts = [row.timestamp_ms for row in features]
    label_by_ts = {label.timestamp_ms: label for label in labels}
    if feature_ts != sorted(feature_ts):
        issues.append(LeakageIssue("features_not_chronological", "feature rows must be chronological"))
    duplicate_count = len(feature_ts) - len(set(feature_ts))
    if duplicate_count:
        issues.append(LeakageIssue("duplicate_feature_timestamps", "feature rows contain duplicate timestamps"))
    gap_count = _gap_count(feature_ts)
    for row in features:
        label = label_by_ts.get(row.timestamp_ms)
        if label and label.horizon_bars > label_horizon:
            issues.append(LeakageIssue("label_horizon_exceeds_manifest", "label horizon exceeds manifest horizon"))
            break
        if label and label.timestamp_ms < row.timestamp_ms:
            issues.append(LeakageIssue("future_feature_timestamp", "label timestamp is earlier than feature timestamp"))
            break
    ranges = [
        ("train", _range_from_rows(train_rows)),
        ("validation", _range_from_rows(validation_rows)),
        ("test", _range_from_rows(test_rows)),
    ]
    for name, item in ranges:
        if item["count"] == 0:
            issues.append(LeakageIssue(f"{name}_empty", f"{name} split is empty"))
    if all(item["count"] for _, item in ranges):
        train_end = ranges[0][1]["end"]
        validation_start = ranges[1][1]["start"]
        validation_end = ranges[1][1]["end"]
        test_start = ranges[2][1]["start"]
        if train_end is not None and validation_start is not None and train_end >= validation_start:
            issues.append(LeakageIssue("train_validation_overlap", "train and validation ranges overlap"))
        if validation_end is not None and test_start is not None and validation_end >= test_start:
            issues.append(LeakageIssue("validation_test_overlap", "validation and test ranges overlap"))
        if embargo > 0 and train_end is not None and validation_start is not None:
            if validation_start - train_end < embargo:
                issues.append(LeakageIssue("train_validation_embargo", "train/validation gap is smaller than embargo"))
        if embargo > 0 and validation_end is not None and test_start is not None:
            if test_start - validation_end < embargo:
                issues.append(LeakageIssue("validation_test_embargo", "validation/test gap is smaller than embargo"))
    return LeakageReport("fail" if issues else "pass", issues, gap_count=gap_count, duplicate_count=duplicate_count)


def manifest_checksum(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(redact_payload(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:32]


def _range_from_rows(rows: list[FeatureRow]) -> dict[str, int | None]:
    if not rows:
        return {"start": None, "end": None, "count": 0}
    return {"start": rows[0].timestamp_ms, "end": rows[-1].timestamp_ms, "count": len(rows)}


def _range_from_labels(rows: list[LabelRow]) -> dict[str, int | None]:
    if not rows:
        return {"start": None, "end": None, "count": 0}
    return {"start": rows[0].timestamp_ms, "end": rows[-1].timestamp_ms, "count": len(rows)}


def _range_from_candles(rows: list[Candle]) -> dict[str, int | None]:
    if not rows:
        return {"start": None, "end": None, "count": 0}
    return {"start": rows[0].open_time_ms, "end": rows[-1].close_time_ms, "count": len(rows)}


def _gap_count(timestamps: list[int]) -> int:
    if len(timestamps) < 3:
        return 0
    deltas = [right - left for left, right in zip(timestamps, timestamps[1:]) if right > left]
    if not deltas:
        return 0
    expected = min(deltas)
    return sum(1 for delta in deltas if delta > expected)
