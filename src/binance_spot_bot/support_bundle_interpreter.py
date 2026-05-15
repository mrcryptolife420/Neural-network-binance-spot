from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from .redaction import redact_payload


def interpret_support_bundle_manifest(path: Path | str) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        return {"status": "warn", "findings": ["missing support bundle manifest"], "recommendations": ["run support-bundle"], "live_trading_enabled": False}
    try:
        if path.suffix.lower() == ".zip":
            with ZipFile(path) as archive:
                manifest_name = "manifest.json" if "manifest.json" in archive.namelist() else ""
                if not manifest_name:
                    return {"status": "warn", "findings": ["missing manifest.json in support bundle"], "live_trading_enabled": False}
                payload = json.loads(archive.read(manifest_name).decode("utf-8"))
        else:
            payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return {"status": "blocked", "findings": ["invalid manifest json"], "live_trading_enabled": False}
    files = payload.get("files", [])
    return redact_payload(
        {
            "status": "ok",
            "sections": [{"name": "manifest", "file_count": len(files) if isinstance(files, list) else files}],
            "findings": [],
            "recommendations": ["verify support bundle before sharing locally"],
            "no_live_summary": "support bundles are local evidence only",
            "live_trading_enabled": False,
        }
    )


def support_bundle_interpreter(status: str) -> dict[str, Any]:
    return {"status": "ok", "interpretation": status, "live_trading_enabled": False}
