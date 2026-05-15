from __future__ import annotations

import hashlib
import time
from typing import Any

from .redaction import redact_payload


PAPER_SIGNOFF_CONFIRM = "PAPER_OS_SIGNOFF"
PAPER_APPROVAL_CONFIRM = "APPROVE_PAPER_OS_ONLY"


def operator_signoff_draft(blockers: list[str] | None = None, warnings: list[str] | None = None) -> dict[str, Any]:
    blockers = blockers or []
    warnings = warnings or []
    checklist = {
        "no_live_proof_reviewed": False,
        "check_all_reviewed": False,
        "dashboard_smoke_reviewed": False,
        "paper_simulation_reviewed": False,
        "data_model_portfolio_traceability_reviewed": False,
        "backup_restore_preview_reviewed": False,
        "release_simulation_reviewed": False,
        "next_roadmap_selected": False,
    }
    return {
        "status": "draft",
        "checklist": checklist,
        "blockers": blockers,
        "warnings": warnings,
        "approval_scope": "paper_ops_only",
        "live_trading_enabled": False,
    }


def approve_operator_signoff(
    confirm: str,
    *,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    blockers = blockers or []
    warnings = warnings or []
    if "live" in notes.lower():
        return {"status": "blocked", "reason": "live approval wording is not allowed", "live_trading_enabled": False}
    if confirm not in {PAPER_SIGNOFF_CONFIRM, PAPER_APPROVAL_CONFIRM}:
        return {"status": "blocked", "reason": "missing paper-only confirm phrase", "live_trading_enabled": False}
    status = "approved_with_warnings" if warnings else "approved_for_paper_ops"
    if blockers:
        status = "blocked"
    payload = {
        "status": "signed" if confirm == PAPER_SIGNOFF_CONFIRM and not blockers else status,
        "approval_scope": "paper_ops_only",
        "blockers": blockers,
        "warnings": warnings,
        "notes": notes,
        "signed_at_ms": int(time.time() * 1000),
        "live_trading_enabled": False,
    }
    payload["signature_hash"] = hashlib.sha256(repr(sorted(payload.items())).encode("utf-8")).hexdigest()[:16]
    return redact_payload(payload)


def operator_signoff(confirm: str) -> dict[str, Any]:
    return approve_operator_signoff(confirm)
