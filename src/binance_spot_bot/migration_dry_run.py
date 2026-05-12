from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .migration_registry import migration_plan
from .redaction import redact_payload


def migration_dry_run(name: str, *, root: Path | str = "data", from_version: str = "0.1.0", to_version: str = "0.2.0") -> dict[str, Any]:
    root = Path(root)
    plan = migration_plan(from_version, to_version)
    affected = [str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()] if root.exists() else []
    payload = {
        "status": "ok" if plan["status"] == "ok" else "blocked",
        "dry_run_id": f"dry-{name}-{int(time.time() * 1000)}",
        "migration": name,
        "plan": plan,
        "creates": ["releases/current-install-fingerprint.json"],
        "updates": affected[:100],
        "deletes": [],
        "destructive": False,
        "source_modified": False,
        "live_trading_enabled": False,
    }
    out = root / "releases" / "migrations"
    out.mkdir(parents=True, exist_ok=True)
    (out / "migration-dry-run.json").write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return redact_payload(payload)
