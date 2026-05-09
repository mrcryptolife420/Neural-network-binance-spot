from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .signal_model import TinyNeuralSignalModel


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
    ) -> ModelMetadata:
        model_id = f"model-{int(time.time() * 1000)}-{uuid.uuid4().hex[:6]}"
        artifact = self.root / model_id / "model.json"
        model.save(artifact)
        metadata = ModelMetadata(
            model_id=model_id,
            model_type="tiny-neural-signal",
            feature_set_version=feature_set_version,
            dataset_id=dataset_id,
            train_range=train_range,
            validation_range=validation_range,
            test_range=test_range,
            metrics=metrics or {},
            created_at_ms=int(time.time() * 1000),
            artifact_path=str(artifact),
            alias=alias,
            status=alias,
        )
        payload = self._load()
        payload["models"].append(asdict(metadata))
        payload.setdefault("aliases", {})[alias] = model_id
        self._write(payload)
        return metadata

    def list_models(self) -> list[ModelMetadata]:
        return [ModelMetadata(**item) for item in self._load().get("models", [])]

    def get_by_alias(self, alias: str) -> ModelMetadata | None:
        payload = self._load()
        model_id = payload.get("aliases", {}).get(alias)
        if not model_id:
            return None
        for item in payload.get("models", []):
            if item["model_id"] == model_id:
                return ModelMetadata(**item)
        return None

    def load_by_alias(self, alias: str) -> tuple[TinyNeuralSignalModel, ModelMetadata] | None:
        metadata = self.get_by_alias(alias)
        if metadata is None:
            return None
        model = TinyNeuralSignalModel.load(Path(metadata.artifact_path))
        model.model_version = metadata.model_id
        return model, metadata

    def _load(self) -> dict[str, Any]:
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def _write(self, payload: dict[str, Any]) -> None:
        self.registry_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
