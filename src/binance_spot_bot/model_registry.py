from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload
from .signal_model import TinyNeuralSignalModel


@dataclass(frozen=True)
class PromotionGateResult:
    allowed: bool
    checks: dict[str, bool]
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModelMetadata:
    model_id: str
    model_type: str
    feature_set_version: str
    dataset_id: str
    train_range: str
    validation_range: str
    test_range: str
    metrics: dict[str, Any]
    created_at_ms: int
    artifact_path: str
    alias: str = "candidate"
    status: str = "candidate"
    role: str = "candidate"
    feature_schema_hash: str = "unknown"
    manifest_path: str = ""
    walkforward_report_path: str = ""
    model_card_path: str = ""
    promotion_decision: dict[str, Any] = field(default_factory=dict)
    previous_champion_id: str = ""


class ModelRegistry:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.registry_path = self.root / "registry.json"
        if not self.registry_path.exists():
            self.registry_path.write_text(json.dumps({"models": [], "aliases": {}}, indent=2), encoding="utf-8")

    def register(
        self,
        model: TinyNeuralSignalModel,
        *,
        alias: str,
        dataset_id: str,
        feature_set_version: str = "features-v1",
        train_range: str = "demo-train",
        validation_range: str = "demo-validation",
        test_range: str = "demo-test",
        metrics: dict[str, Any] | None = None,
        role: str = "candidate",
        feature_schema_hash: str = "unknown",
        manifest_path: str = "",
        walkforward_report_path: str = "",
    ) -> ModelMetadata:
        model_id = f"model-{int(time.time() * 1000)}-{uuid.uuid4().hex[:6]}"
        artifact = self.root / model_id / "model.json"
        model.save(artifact)
        metrics = metrics or {}
        metadata = ModelMetadata(
            model_id=model_id,
            model_type="tiny-neural-signal",
            feature_set_version=feature_set_version,
            dataset_id=dataset_id,
            train_range=train_range,
            validation_range=validation_range,
            test_range=test_range,
            metrics=metrics,
            created_at_ms=int(time.time() * 1000),
            artifact_path=str(artifact),
            alias=alias,
            status=role,
            role=role,
            feature_schema_hash=feature_schema_hash,
            manifest_path=manifest_path,
            walkforward_report_path=walkforward_report_path,
        )
        model_card_path = self.write_model_card(metadata)
        metadata = ModelMetadata(**{**asdict(metadata), "model_card_path": str(model_card_path)})
        payload = self._load()
        payload["models"].append(asdict(metadata))
        payload.setdefault("aliases", {})[alias] = model_id
        self._write(payload)
        return metadata

    def list_models(self) -> list[ModelMetadata]:
        return [ModelMetadata(**_metadata_defaults(item)) for item in self._load().get("models", [])]

    def get_by_alias(self, alias: str) -> ModelMetadata | None:
        payload = self._load()
        model_id = payload.get("aliases", {}).get(alias)
        if not model_id:
            return None
        for item in payload.get("models", []):
            if item["model_id"] == model_id:
                return ModelMetadata(**_metadata_defaults(item))
        return None

    def get_by_id(self, model_id: str) -> ModelMetadata | None:
        for item in self._load().get("models", []):
            if item["model_id"] == model_id:
                return ModelMetadata(**_metadata_defaults(item))
        return None

    def load_by_alias(self, alias: str) -> tuple[TinyNeuralSignalModel, ModelMetadata] | None:
        metadata = self.get_by_alias(alias)
        if metadata is None:
            return None
        model = TinyNeuralSignalModel.load(Path(metadata.artifact_path))
        model.model_version = metadata.model_id
        return model, metadata

    def evaluate_promotion(self, metadata: ModelMetadata, *, operator_confirmed: bool = False) -> PromotionGateResult:
        metrics = metadata.metrics
        max_drawdown = _float(metrics.get("max_drawdown_quote", 0))
        max_allowed_drawdown = _float(metrics.get("max_allowed_drawdown_quote", 1000))
        trade_count = int(metrics.get("trade_count", metrics.get("trades", 0)) or 0)
        min_trade_count = int(metrics.get("min_trade_count", 1) or 1)
        checks = {
            "dataset_manifest_present": bool(metadata.dataset_id and metadata.manifest_path),
            "leakage_guard_passed": bool(metrics.get("leakage_pass", False)),
            "feature_schema_hash_present": bool(metadata.feature_schema_hash and metadata.feature_schema_hash != "unknown"),
            "walkforward_report_present": bool(metadata.walkforward_report_path),
            "beats_baseline_after_costs": bool(metrics.get("candidate_beats_baseline", False)),
            "drawdown_within_limit": max_drawdown <= max_allowed_drawdown,
            "minimum_trade_count": trade_count >= min_trade_count,
            "model_card_present": bool(metadata.model_card_path),
            "operator_confirmed": operator_confirmed,
        }
        reasons = [name for name, passed in checks.items() if not passed]
        return PromotionGateResult(not reasons, checks, reasons)

    def promote_to_champion(self, model_id: str, *, operator_confirmed: bool = False) -> PromotionGateResult:
        payload = self._load()
        target = None
        previous_champion = payload.get("aliases", {}).get("champion", "")
        for item in payload.get("models", []):
            if item["model_id"] == model_id:
                target = item
                break
        if target is None:
            return PromotionGateResult(False, {"model_exists": False}, ["model_exists"])
        metadata = ModelMetadata(**_metadata_defaults(target))
        decision = self.evaluate_promotion(metadata, operator_confirmed=operator_confirmed)
        target["promotion_decision"] = decision.to_dict()
        if not decision.allowed:
            self._write(payload)
            return decision
        for item in payload.get("models", []):
            if item.get("status") == "champion" or item.get("role") == "champion":
                item["status"] = "archived"
                item["role"] = "archived"
        target["status"] = "champion"
        target["role"] = "champion"
        target["alias"] = "champion"
        target["previous_champion_id"] = previous_champion
        payload.setdefault("aliases", {})["champion"] = model_id
        self._write(payload)
        self.write_model_card(ModelMetadata(**_metadata_defaults(target)))
        return decision

    def write_model_card(self, metadata: ModelMetadata) -> Path:
        path = self.root / metadata.model_id / "model-card.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = redact_payload(
            {
                "model_id": metadata.model_id,
                "role": metadata.role,
                "status": metadata.status,
                "dataset_id": metadata.dataset_id,
                "feature_schema_hash": metadata.feature_schema_hash,
                "training_config": {
                    "model_type": metadata.model_type,
                    "feature_set_version": metadata.feature_set_version,
                },
                "ranges": {
                    "train": metadata.train_range,
                    "validation": metadata.validation_range,
                    "test": metadata.test_range,
                },
                "walk_forward_summary": metadata.metrics,
                "baseline_comparison": {
                    "candidate_beats_baseline": bool(metadata.metrics.get("candidate_beats_baseline", False)),
                },
                "known_limitations": ["paper/shadow validation only", "not financial advice", "not live-trading approved"],
                "intended_use": "offline evaluation, paper trading, and shadow-only research",
                "forbidden_use": "live trading without a later roadmap, readiness gate, and manual approval",
                "created_at_ms": metadata.created_at_ms,
                "operator_notes": "",
            }
        )
        path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")
        return path

    def _load(self) -> dict[str, Any]:
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def _write(self, payload: dict[str, Any]) -> None:
        self.registry_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _metadata_defaults(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "role": item.get("status", "candidate"),
        "feature_schema_hash": "unknown",
        "manifest_path": "",
        "walkforward_report_path": "",
        "model_card_path": "",
        "promotion_decision": {},
        "previous_champion_id": "",
        **item,
    }


def _float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
