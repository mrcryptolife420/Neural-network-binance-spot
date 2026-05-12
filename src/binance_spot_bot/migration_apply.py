from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .migration_dry_run import migration_dry_run
from .pre_upgrade_backup_gate import pre_upgrade_backup_gate
from .redaction import redact_payload


def migration_apply(name: str, confirm: str, *, root: Path | str = "data", backup: Path | None = None, require_backup: bool = False) -> dict[str, Any]:
    if confirm != "APPLY_LOCAL_MIGRATION":
        return {"status": "blocked", "reason": "confirm_required", "live_trading_enabled": False}
    root = Path(root)
    dry_run = migration_dry_run(name, root=root)
    if dry_run["status"] != "ok":
        return {"status": "blocked", "reason": "dry_run_failed", "dry_run": dry_run, "live_trading_enabled": False}
    if require_backup:
        gate = pre_upgrade_backup_gate(backup or root / "disaster-recovery" / "backup.zip")
        if gate["status"] != "ok":
            return {"status": "blocked", "reason": "backup_gate_failed", "backup_gate": gate, "live_trading_enabled": False}
    out = root / "releases" / "migrations"
    out.mkdir(parents=True, exist_ok=True)
    result = {"status": "applied", "migration": name, "applied_at_ms": int(time.time() * 1000), "dry_run": dry_run["dry_run_id"], "rollback_marker": str(out / "rollback-marker.json"), "live_trading_enabled": False}
    (out / "migration-journal.jsonl").open("a", encoding="utf-8").write(json.dumps(redact_payload(result), default=str) + "\n")
    (out / "rollback-marker.json").write_text(json.dumps({"migration": name, "restore": "pre-upgrade backup", "live_trading_enabled": False}, indent=2), encoding="utf-8")
    return redact_payload(result)
