from __future__ import annotations

from binance_spot_bot.portfolio_lab.common import now_ms, stable_hash

from . import LIVE_SCALING_APPROVAL_CONFIRM


def operator_approval_workflow(confirm: str):
    return {"status": "approved" if confirm == "APPROVE_LIVE_SCALING_REVIEW" else "blocked", "one_time": True, "live_trading_enabled": False}


def create_operator_approval_request(decision: str, evidence_ref: str) -> dict[str, object]:
    payload = {"decision": decision, "evidence_ref": evidence_ref, "created_at_ms": now_ms()}
    return {"status": "pending", "request_id": f"approval-{stable_hash(payload)[:12]}", "payload": payload, "live_trading_enabled": False}


def decide_operator_approval(request: dict[str, object], *, confirm: str, note: str) -> dict[str, object]:
    blockers = []
    if confirm != LIVE_SCALING_APPROVAL_CONFIRM:
        blockers.append(f"confirm required: {LIVE_SCALING_APPROVAL_CONFIRM}")
    if not note:
        blockers.append("operator note required")
    return {"status": "blocked" if blockers else "approved", "request_id": request.get("request_id"), "blockers": blockers, "one_time": True, "approval_token": stable_hash(request)[:16] if not blockers else "", "live_trading_enabled": False}
