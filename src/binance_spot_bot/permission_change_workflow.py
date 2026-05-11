from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .permission_profiles import FORBIDDEN_SCOPES
from .redaction import redact_payload


def permission_change_workflow(role: str, change: str) -> dict[str, Any]:
    return propose_permission_change(role, {"change": change})


def propose_permission_change(role: str, proposed: dict[str, Any]) -> dict[str, Any]:
    scopes = set(_flatten(proposed))
    forbidden = sorted(scopes & FORBIDDEN_SCOPES)
    change_id = f"perm-{int(time.time() * 1000)}"
    return redact_payload(
        {
            "status": "blocked" if forbidden else "approval_required",
            "change_id": change_id,
            "role": role,
            "diff": {"proposed": proposed},
            "validation": {"allowed": not forbidden, "forbidden_scopes": forbidden},
            "confirm_phrase": "PERMISSION_CHANGE",
            "live_trading_enabled": False,
        }
    )


def approve_permission_change(change: dict[str, Any], *, role: str, confirm: str, out: Path) -> dict[str, Any]:
    if role != "admin_local" or confirm != "PERMISSION_CHANGE" or change.get("status") == "blocked":
        return {"status": "blocked", "reason": "admin_confirm_required_or_invalid_change", "live_trading_enabled": False}
    out.parent.mkdir(parents=True, exist_ok=True)
    rollback = out.with_suffix(".rollback.json")
    rollback.write_text(json.dumps({"rollback_for": change["change_id"]}, indent=2), encoding="utf-8")
    out.write_text(json.dumps(redact_payload(change), indent=2, default=str), encoding="utf-8")
    return {"status": "ok", "path": str(out), "rollback": str(rollback), "live_trading_enabled": False}


def _flatten(value: Any) -> list[str]:
    if isinstance(value, dict):
        out: list[str] = []
        for item in value.values():
            out.extend(_flatten(item))
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(_flatten(item))
        return out
    return [str(value)]
