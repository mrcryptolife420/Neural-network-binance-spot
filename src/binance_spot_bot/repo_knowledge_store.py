from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _short_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:24]


def write_repo_knowledge_store(root: Path, payload: dict) -> dict[str, str]:
    out = root / "data" / "repository-knowledge"
    out.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, value in payload.items():
        file = out / f"{name}.json"
        file.write_text(json.dumps({"status": "ready", "payload": value, "live_trading_enabled": False}, indent=2, default=str), encoding="utf-8")
        paths[name] = str(file)
    manifest = {"status": "ready", "files": [{"name": key, "path": value, "sha256": _short_hash(Path(value))} for key, value in paths.items()], "live_trading_enabled": False}
    manifest_path = out / "knowledge-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    paths["manifest"] = str(manifest_path)
    return paths


def verify_repo_knowledge_store(manifest_path: Path | str) -> dict[str, Any]:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    errors = []
    for item in manifest.get("files", []):
        path = Path(item["path"])
        if not path.exists() or _short_hash(path) != item["sha256"]:
            errors.append(item["name"])
    return {"status": "ok" if not errors else "failed", "errors": errors, "live_trading_enabled": False}
