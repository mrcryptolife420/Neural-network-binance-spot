from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from statistics import mean, pstdev
from typing import Any

from .types import Candle, FeatureRow


@dataclass(frozen=True)
class DataQualityIssue:
    severity: str
    code: str
    message: str
    details: dict[str, Any]


@dataclass(frozen=True)
class DataQualityReport:
    status: str
    issues: list[DataQualityIssue]
    checked_rows: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "checked_rows": self.checked_rows,
            "issues": [asdict(issue) for issue in self.issues],
        }


def check_candles(
    candles: list[Candle],
    *,
    expected_interval_ms: int = 60_000,
    max_stale_ms: int = 120_000,
    now_ms: int | None = None,
    spread_bps: Decimal | None = None,
    max_spread_bps: Decimal = Decimal("30"),
) -> DataQualityReport:
    issues: list[DataQualityIssue] = []
    if not candles:
        issues.append(DataQualityIssue("warning", "missing_candles", "no candles available", {}))
        return DataQualityReport("degraded", issues, 0)
    timestamps = [c.open_time_ms for c in candles]
    duplicate_count = len(timestamps) - len(set(timestamps))
    if duplicate_count:
        issues.append(DataQualityIssue("error", "duplicate_timestamps", "duplicate candles detected", {"count": duplicate_count}))
    if timestamps != sorted(timestamps):
        issues.append(DataQualityIssue("error", "non_monotonic_timestamps", "candles are not chronological", {}))
    gaps = [
        (timestamps[i - 1], timestamps[i])
        for i in range(1, len(timestamps))
        if timestamps[i] - timestamps[i - 1] > expected_interval_ms * 2
    ]
    if gaps:
        issues.append(DataQualityIssue("warning", "missing_candles", "time gaps detected", {"count": len(gaps)}))
    zero_prices = sum(1 for c in candles if min(c.open, c.high, c.low, c.close) <= 0)
    if zero_prices:
        issues.append(DataQualityIssue("error", "zero_or_negative_prices", "zero or negative prices detected", {"count": zero_prices}))
    if now_ms is not None and candles[-1].close_time_ms is not None:
        age = now_ms - candles[-1].close_time_ms
        if age > max_stale_ms:
            issues.append(DataQualityIssue("warning", "stale_data", "latest candle is stale", {"age_ms": age}))
    if spread_bps is not None and spread_bps > max_spread_bps:
        issues.append(DataQualityIssue("warning", "extreme_spread", "spread exceeds configured threshold", {"spread_bps": str(spread_bps)}))
    status = "ok"
    if any(issue.severity == "warning" for issue in issues):
        status = "degraded"
    if any(issue.severity == "error" for issue in issues):
        status = "unhealthy"
    return DataQualityReport(status, issues, len(candles))


def feature_shift(reference: list[FeatureRow], current: list[FeatureRow], threshold: float = 0.25) -> DataQualityReport:
    issues: list[DataQualityIssue] = []
    if not reference or not current:
        return DataQualityReport("degraded", [DataQualityIssue("warning", "missing_features", "reference or current features missing", {})], 0)
    for name in sorted(reference[0].values.keys()):
        ref_values = [row.values.get(name, 0.0) for row in reference]
        cur_values = [row.values.get(name, 0.0) for row in current]
        ref_mean = mean(ref_values)
        cur_mean = mean(cur_values)
        ref_std = pstdev(ref_values) or 1.0
        score = abs(cur_mean - ref_mean) / ref_std
        if score > threshold:
            issues.append(
                DataQualityIssue(
                    "warning",
                    "feature_shift",
                    f"feature distribution shifted: {name}",
                    {"feature": name, "score": round(score, 6), "reference_mean": ref_mean, "current_mean": cur_mean},
                )
            )
    return DataQualityReport("degraded" if issues else "ok", issues, len(current))
