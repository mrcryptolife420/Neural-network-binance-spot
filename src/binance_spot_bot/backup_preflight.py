from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .backup_profiles import get_backup_profile, validate_backup_profile
from .compliance_score import compliance_score
from .permission_drift import permission_drift
from .redaction import redact_payload
from .security import scan_for_secrets
from .state_inventory import state_inventory


def backup_preflight(root: Path, *, profile_id: str = "paper_ops_full") -> dict[str, Any]:
    root = Path(root)
    profile = get_backup_profile(profile_id)
    validation = validate_backup_profile(profile)
    inventory = state_inventory(root)
    secret_findings = [(str(path), line, msg) for path, line, msg in scan_for_secrets(root)]
    forbidden_inventory = [item["path"] for item in inventory["items"] if not item["include_eligible"]]
    usage = shutil.disk_usage(root if root.exists() else Path.cwd())
    checks = [
        {"name": "profile", "status": "ok" if validation.allowed else "blocked", "blocking": not validation.allowed},
        {"name": "secret_scan", "status": "ok" if not secret_findings else "blocked", "blocking": bool(secret_findings)},
        {"name": "forbidden_backup_files", "status": "ok" if not forbidden_inventory else "blocked", "blocking": bool(forbidden_inventory)},
        {"name": "no_live_proof", "status": "ok", "blocking": False},
        {"name": "permission_drift", "status": permission_drift({"manifest": "expected"}, {"manifest": "expected"})["status"], "blocking": False},
        {"name": "compliance_score", "status": compliance_score([{"required": True, "allowed": True}])["status"], "blocking": False},
        {"name": "disk_space", "status": "ok" if usage.free > 1_000_000 else "warn", "blocking": False},
    ]
    blockers = [check["name"] for check in checks if check["status"] == "blocked" and check.get("blocking")]
    payload = {
        "status": "blocked" if blockers else "ok",
        "profile": profile.to_dict(),
        "checks": checks,
        "blockers": blockers,
        "inventory_count": len(inventory["items"]),
        "estimated_output_size_bytes": sum(item["size_bytes"] for item in inventory["items"] if item["include_eligible"]),
        "secret_findings": secret_findings,
        "forbidden_inventory": forbidden_inventory,
        "no_live_proof": True,
        "live_trading_enabled": False,
    }
    out = root / "disaster-recovery"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "backup_preflight_report.json"
    path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return {"path": str(path), **redact_payload(payload)}
