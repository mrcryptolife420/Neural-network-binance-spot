from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:24]


def save_profile_run(root: Path | str, run: dict[str, Any]) -> dict[str, Any]:
    root_path = Path(root)
    out = root_path / "data" / "performance" / "runs"
    out.mkdir(parents=True, exist_ok=True)
    run_id = run.get("run_id", "latest")
    path = out / f"{run_id}.json"
    payload = {**run, "live_trading_enabled": False}
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    latest = root_path / "data" / "performance" / "latest.json"
    latest.parent.mkdir(parents=True, exist_ok=True)
    latest.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    manifest = {"status": "ready", "run_id": run_id, "path": str(path), "sha256": _hash_file(path), "live_trading_enabled": False}
    manifest_path = root_path / "data" / "performance" / "manifests" / f"{run_id}-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    manifest["manifest"] = str(manifest_path)
    return manifest


def load_profile_run(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify_performance_manifest(manifest_path: Path | str) -> dict[str, Any]:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    path = Path(manifest["path"])
    ok = path.exists() and _hash_file(path) == manifest["sha256"]
    return {"status": "ok" if ok else "failed", "live_trading_enabled": False}


def write_performance_store(root: Path, payload: dict) -> dict[str, str]:
    manifest = save_profile_run(root, payload)
    return {"manifest": manifest["manifest"], "path": manifest["path"]}
