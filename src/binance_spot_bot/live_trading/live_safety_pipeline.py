from __future__ import annotations

from pathlib import Path
from typing import Any

from . import LIVE_RISK_CONFIRM, REAL_ORDER_CONFIRM
from .first_live_order_gate import evaluate_first_live_order_gate
from .live_account_verifier import verify_live_read_only_account
from .live_arm_token import create_live_arm_token
from .live_audit import append_live_audit_event, verify_live_audit_chain
from .live_dry_run_session import run_live_dry_run_session
from .live_endpoint_policy import live_endpoint_policy_report
from .live_evidence_prerequisite_gate import evaluate_live_evidence_prerequisites, fixture_live_evidence, write_live_evidence_prerequisite_report
from .live_execution_adapter import FakeFirstOrderAdapter
from .live_execution_evidence import export_live_execution_evidence
from .live_order_preview import build_live_order_preview
from .live_order_sizing_guard import evaluate_live_order_sizing
from .live_safety_drills import run_live_cancel_drill, run_live_kill_switch_drill


def run_live_safety_pipeline(root: Path, *, arm_confirm: str = LIVE_RISK_CONFIRM, order_confirm: str = "", execute_first_order: bool = False) -> dict[str, Any]:
    evidence = evaluate_live_evidence_prerequisites(fixture_live_evidence())
    write_live_evidence_prerequisite_report(root, evidence)
    account = verify_live_read_only_account()
    policy = live_endpoint_policy_report("dry_run", ["server_time", "get_account_state", "local_order_preview"])
    dry_run = run_live_dry_run_session(fixture_live_evidence())
    preview = build_live_order_preview({"symbol": "BTCUSDT", "side": "BUY", "quote": 5})
    sizing = evaluate_live_order_sizing(preview, max_balance_pct=0.10)
    kill_switch = run_live_kill_switch_drill()
    cancel = run_live_cancel_drill()
    context = {"evidence": evidence, "account": account, "dry_run": dry_run, "preview": preview, "sizing": sizing, "kill_switch_drill": kill_switch, "cancel_drill": cancel}
    arm_token = create_live_arm_token(context, confirm=arm_confirm)
    context["arm_token"] = arm_token
    first_order = evaluate_first_live_order_gate(context, confirm=order_confirm, adapter=FakeFirstOrderAdapter()) if execute_first_order else {"status": "blocked", "blockers": ["first live order execute not requested"], "live_order_submitted": False, "live_trading_enabled": False}
    audit_chain: list[dict[str, Any]] = []
    for event_type, payload in [("evidence_checked", evidence), ("account_verified", account), ("dry_run_completed", dry_run), ("order_preview_created", preview), ("arm_token_created", arm_token), ("first_order_gate", first_order)]:
        append_live_audit_event(audit_chain, event_type, payload)
    audit = verify_live_audit_chain(audit_chain)
    evidence_bundle = export_live_execution_evidence(root, {"run_id": "live-safety-pipeline", "dry_run": dry_run, "first_order": first_order, "audit": audit, "live_trading_enabled": False})
    return {"status": "ok", "evidence": evidence, "account": account, "endpoint_policy": policy, "dry_run": dry_run, "preview": preview, "sizing": sizing, "kill_switch_drill": kill_switch, "cancel_drill": cancel, "arm_token": arm_token, "first_order": first_order, "audit": audit, "evidence_bundle": evidence_bundle, "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}
