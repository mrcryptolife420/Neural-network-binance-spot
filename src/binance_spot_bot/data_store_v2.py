from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload

ALLOWED_SUFFIXES = {".json", ".jsonl", ".csv", ".md", ".txt"}


@dataclass(frozen=True)
class DataArtifactRef:
    artifact_id: str
    path: str
    artifact_type: str
    schema_version: str
    sha256: str
    rows: int = 0
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class DataStoreManifest:
    manifest_id: str
    created_at_ms: int
    artifacts: list[DataArtifactRef] = field(default_factory=list)
    no_secret_proof: bool = True
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class DataStorePathPolicy:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()

    def resolve(self, relative: str | Path) -> Path:
        target = (self.root / relative).resolve()
        if target != self.root and self.root not in target.parents:
            raise ValueError("data path outside root")
        if target.suffix and target.suffix.lower() not in ALLOWED_SUFFIXES:
            raise ValueError(f"unsupported suffix: {target.suffix}")
        return target


class DataStoreRoot:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.policy = DataStorePathPolicy(self.root)
        for name in ["raw", "candles", "features", "labels", "manifests", "quality", "lineage"]:
            (self.root / name).mkdir(parents=True, exist_ok=True)

    def write_json(self, relative: str | Path, payload: dict[str, Any]) -> DataArtifactRef:
        path = self.policy.resolve(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        safe = redact_payload(payload)
        path.write_text(json.dumps(safe, indent=2, sort_keys=True, default=str), encoding="utf-8")
        return self.artifact_ref(path, "json", rows=1)

    def write_jsonl(self, relative: str | Path, rows: list[dict[str, Any]], artifact_type: str) -> DataArtifactRef:
        path = self.policy.resolve(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(redact_payload(row), sort_keys=True, default=str) + "\n")
        return self.artifact_ref(path, artifact_type, rows=len(rows))

    def artifact_ref(self, path: Path, artifact_type: str, rows: int = 0, schema_version: str = "data-store-v2") -> DataArtifactRef:
        return DataArtifactRef(
            artifact_id=path.stem,
            path=str(path),
            artifact_type=artifact_type,
            schema_version=schema_version,
            sha256=_sha256(path),
            rows=rows,
        )

    def write_manifest(self, manifest_id: str, artifacts: list[DataArtifactRef]) -> Path:
        manifest = DataStoreManifest(manifest_id, int(time.time() * 1000), artifacts)
        path = self.policy.resolve(Path("manifests") / f"{manifest_id}.json")
        path.write_text(json.dumps(manifest.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        return path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:24]
