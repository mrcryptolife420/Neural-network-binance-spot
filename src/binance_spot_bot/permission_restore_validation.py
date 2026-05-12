from __future__ import annotations

from pathlib import Path
from typing import Any

from .permission_drift import permission_drift
from .permission_profiles import FORBIDDEN_SCOPES
from .redaction import redact_payload


def permission_restore_validate(root: Path) -> dict[str, Any]:
    permissions = Path(root) / "permissions"
    action_center = Path(root) / "action-center"
    blockers = []
    warnings = []
    if not permissions.exists():
        warnings.append("permissions_missing")
    if not action_center.exists():
        warnings.append("action_journal_missing")
    for path in Path(root).rglob("*.json") if Path(root).exists() else []:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(scope in text for scope in FORBIDDEN_SCOPES):
            blockers.append(f"forbidden_scope:{path.name}")
        if '"live_trading_enabled": true' in text.lower():
            blockers.append(f"live_enabled:{path.name}")
    drift = permission_drift({"manifest": "expected"}, {"manifest": "expected"})
    return redact_payload({"status": "blocked" if blockers else ("warn" if warnings else "ok"), "blockers": blockers, "warnings": warnings, "permission_drift": drift, "no_live_proof": not blockers, "live_trading_enabled": False})
