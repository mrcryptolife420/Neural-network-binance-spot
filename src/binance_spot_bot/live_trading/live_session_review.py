from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, now_ms, redact_value, stable_hash, status_from_blockers

from . import NO_AUTO_SCALE_STATEMENT, NOT_FINANCIAL_ADVICE_STATEMENT
from .safety import LiveSafetyDecision, no_live_order


def live_session_review(evidence_present: bool, unknown_order_state: bool = False):
    return {**LiveSafetyDecision("blocked" if not evidence_present or unknown_order_state else "ok", "review", [r for r, flag in {"missing_evidence": not evidence_present, "unknown_order_state": unknown_order_state}.items() if flag]).to_dict(), **no_live_order()}


def fixture_review_input() -> dict[str, Any]:
    return {
        "session_id": "live-session-fixture",
        "live_session_evidence_manifest_path": "data/live-trading/session-evidence/fixture/manifest.json",
        "session_plan_path": "data/live-trading/sessions/plans/fixture.json",
        "live_orders_exist": True,
        "order_states": ["reconciled"],
        "reconciliation_report_paths": ["data/live-trading/sessions/reconciliation/fixture.json"],
        "evidence_hash_ok": True,
        "risk_limits_used": {"max_session_orders": 2},
        "scaling_level_used": 1,
        "no_auto_scale_statement": NO_AUTO_SCALE_STATEMENT,
        "not_financial_advice_statement": NOT_FINANCIAL_ADVICE_STATEMENT,
    }


def run_live_session_review(review_input: dict[str, Any]) -> dict[str, Any]:
    payload = redact_value(review_input)
    blockers: list[str] = []
    warnings: list[str] = []
    if not payload.get("live_session_evidence_manifest_path"):
        blockers.append("missing live session evidence manifest")
    if not payload.get("session_plan_path"):
        blockers.append("missing session plan")
    if payload.get("live_orders_exist") and not payload.get("reconciliation_report_paths"):
        blockers.append("missing reconciliation report")
    if "unknown" in payload.get("order_states", []):
        blockers.append("unknown order state")
    if "unreconciled" in payload.get("order_states", []):
        blockers.append("unreconciled order")
    if payload.get("evidence_hash_ok") is False:
        blockers.append("evidence hash mismatch")
    if not payload.get("no_auto_scale_statement"):
        blockers.append("no auto-scale statement missing")
    if not payload.get("not_financial_advice_statement"):
        blockers.append("not financial advice statement missing")
    return {
        "status": status_from_blockers(blockers, warnings),
        "review_id": f"review-{stable_hash(payload)[:12]}",
        "session_id": payload.get("session_id", "unknown"),
        "evidence_integrity_status": "ok" if payload.get("evidence_hash_ok") else "blocked",
        "findings": [{"category": "safety", "message": item, "severity": "P0"} for item in blockers],
        "blockers": blockers,
        "warnings": warnings,
        "score_summary": {"grade": "blocked" if blockers else "pending_scorecard"},
        "eligible_for_scorecard": not blockers,
        "eligible_for_scaling_review": False,
        "no_auto_scale_statement": NO_AUTO_SCALE_STATEMENT,
        "not_financial_advice_statement": NOT_FINANCIAL_ADVICE_STATEMENT,
        "secret_redaction_status": "ok",
        "created_at_ms": now_ms(),
        "live_order_submitted": False,
        "live_trading_enabled": False,
    }


def write_live_session_review_report(root: Path, report: dict[str, Any]) -> dict[str, Any]:
    return json_write(root / "data" / "live-trading" / "governance" / "reviews" / f"{report['review_id']}.json", report)
