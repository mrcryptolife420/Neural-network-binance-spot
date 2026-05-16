from __future__ import annotations

from pathlib import Path
from typing import Any

from . import CONTROLLED_ORDER_CONFIRM, CONTROLLED_SESSION_CONFIRM
from .automatic_disarm_rules import evaluate_automatic_disarm
from .controlled_live_executor import execute_controlled_live_order
from .live_circuit_breakers import evaluate_live_circuit_breakers
from .live_monitoring import live_monitoring_heartbeat
from .live_order_lifecycle import transition_live_order_lifecycle
from .live_reconciliation import reconcile_live_order
from .live_safety_pipeline import run_live_safety_pipeline
from .live_session_budget import evaluate_live_session_budget
from .live_session_evidence import export_live_session_evidence
from .live_session_manager import arm_controlled_live_session, transition_controlled_live_session
from .live_session_plan import LiveSessionPlan, validate_live_session_plan, write_live_session_plan_report
from .live_session_store import create_live_session, record_live_session_event
from .micro_position_scaling import evaluate_micro_position_scaling


def run_controlled_live_session_pipeline(root: Path, *, arm_confirm: str = CONTROLLED_SESSION_CONFIRM, order_confirm: str = "") -> dict[str, Any]:
    plan = validate_live_session_plan(LiveSessionPlan())
    write_live_session_plan_report(root, plan)
    session = create_live_session(root, plan)
    arm = arm_controlled_live_session(plan, confirm=arm_confirm)
    scaling = evaluate_micro_position_scaling(1, 2, prior_sessions_ok=True, unreconciled_orders=0, recent_emergency_stop=False, approved=True)
    usage = {"orders": 0, "quote_exposure": 5, "single_order_quote": 5, "session_loss_quote": 0, "spread_bps": 5, "data_age_ms": 1_000}
    budget = evaluate_live_session_budget(plan, usage)
    heartbeat = live_monitoring_heartbeat()
    lifecycle = transition_live_order_lifecycle("preview_created", "preview_validated")
    roadmap_118 = run_live_safety_pipeline(root, execute_first_order=False)
    context = {"session_state": "armed", "plan": plan, "roadmap_118_context": {**roadmap_118, "evidence": roadmap_118["evidence"], "account": roadmap_118["account"], "dry_run": roadmap_118["dry_run"], "preview": roadmap_118["preview"], "sizing": roadmap_118["sizing"], "kill_switch_drill": roadmap_118["kill_switch_drill"], "arm_token": roadmap_118["arm_token"]}, "reconciliation_required": False}
    executor = execute_controlled_live_order(context, usage, confirm=order_confirm) if order_confirm else {"status": "blocked", "blockers": ["controlled order execute not requested"], "live_order_submitted": False, "live_trading_enabled": False}
    reconciliation = reconcile_live_order({"order_id": "fake-live-order-1", "status": "FILLED", "executed_qty": 1}, {"order_id": "fake-live-order-1", "status": "FILLED", "executed_qty": 1})
    disarm = evaluate_automatic_disarm([])
    breakers = evaluate_live_circuit_breakers([])
    transition = transition_controlled_live_session("ready_to_arm", "armed")
    record_live_session_event(session["session"], "pipeline", {"plan": plan, "arm": arm, "budget": budget})
    evidence = export_live_session_evidence(root, {"run_id": "controlled-live-session-pipeline", "plan": plan, "session": session, "scaling": scaling, "budget": budget, "heartbeat": heartbeat, "executor": executor, "reconciliation": reconciliation, "disarm": disarm, "breakers": breakers, "live_trading_enabled": False})
    return {"status": "ok", "plan": plan, "session": session, "arm": arm, "scaling": scaling, "budget": budget, "heartbeat": heartbeat, "lifecycle": lifecycle, "executor": executor, "reconciliation": reconciliation, "disarm": disarm, "circuit_breakers": breakers, "transition": transition, "evidence": evidence, "live_trading_enabled": False}
