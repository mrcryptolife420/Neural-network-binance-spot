from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class ModelArtifactManifest:
    model_id: str
    artifact_path: str
    artifact_sha256: str
    feature_schema_hash: str
    dataset_id: str
    metrics: dict[str, Any]
    created_at_ms: int
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def write_model_artifact_manifest(path: Path | str, *, model_id: str, artifact_path: Path | str, feature_schema_hash: str, dataset_id: str, metrics: dict[str, Any]) -> Path:
    artifact = Path(artifact_path)
    manifest = ModelArtifactManifest(model_id, str(artifact), _sha256(artifact), feature_schema_hash, dataset_id, metrics, int(time.time() * 1000))
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest.to_dict(), indent=2, sort_keys=True, default=str), encoding="utf-8")
    return target


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:24]
