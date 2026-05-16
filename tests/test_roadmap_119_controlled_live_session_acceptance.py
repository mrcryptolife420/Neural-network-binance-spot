from __future__ import annotations

import json
from dataclasses import replace

from binance_spot_bot.live_trading import CONTROLLED_ORDER_CONFIRM, CONTROLLED_SESSION_CONFIRM
from binance_spot_bot.live_trading.automatic_disarm_rules import evaluate_automatic_disarm
from binance_spot_bot.live_trading.controlled_live_executor import execute_controlled_live_order
from binance_spot_bot.live_trading.live_circuit_breakers import evaluate_live_circuit_breakers
from binance_spot_bot.live_trading.live_monitoring import live_monitoring_heartbeat
from binance_spot_bot.live_trading.live_order_lifecycle import transition_live_order_lifecycle
from binance_spot_bot.live_trading.live_reconciliation import reconcile_live_order
from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline
from binance_spot_bot.live_trading.live_session_budget import evaluate_live_session_budget
from binance_spot_bot.live_trading.live_session_evidence import export_live_session_evidence
from binance_spot_bot.live_trading.live_session_manager import arm_controlled_live_session, transition_controlled_live_session
from binance_spot_bot.live_trading.live_session_pipeline import run_controlled_live_session_pipeline
from binance_spot_bot.live_trading.live_session_plan import LiveSessionPlan, validate_live_session_plan
from binance_spot_bot.live_trading.live_session_store import create_live_session, record_live_session_event
from binance_spot_bot.live_trading.micro_position_scaling import evaluate_micro_position_scaling


def test_live_session_plan_validation_blocks_missing_refs_budgets_requirements_and_secrets() -> None:
    plan = LiveSessionPlan()
    valid = validate_live_session_plan(plan)
    assert valid["status"] == "ok"
    assert valid["live_trading_enabled"] is False

    missing_117 = validate_live_session_plan(replace(plan, evidence_refs=replace(plan.evidence_refs, roadmap_117_evidence="")))
    assert "missing Roadmap 117 evidence ref" in missing_117["blockers"]
    missing_118 = validate_live_session_plan(replace(plan, evidence_refs=replace(plan.evidence_refs, roadmap_118_evidence="")))
    assert "missing Roadmap 118 evidence ref" in missing_118["blockers"]
    invalid_budget = validate_live_session_plan(replace(plan, budget=replace(plan.budget, max_session_orders=0)))
    assert invalid_budget["status"] == "blocked"
    unsafe = validate_live_session_plan(replace(plan, symbol_scope=replace(plan.symbol_scope, allowed_order_types=["OCO"])))
    assert "unsafe order type" in unsafe["blockers"]
    no_preview = validate_live_session_plan(replace(plan, risk=replace(plan.risk, require_preview_hash=False)))
    assert "preview hash requirement missing" in no_preview["blockers"]
    unsafe = "A" * 64
    redacted_report = validate_live_session_plan(dict(unsafe_value=unsafe))
    assert unsafe not in json.dumps(redacted_report)


def test_session_store_manager_scaling_budget_lifecycle_reconciliation_and_disarm(tmp_path) -> None:
    plan = validate_live_session_plan(LiveSessionPlan())
    session = create_live_session(tmp_path, plan)
    assert session["status"] == "ok"
    assert record_live_session_event(session["session"], "created", {"ok": True})["status"] == "ok"

    assert transition_controlled_live_session("locked", "plan_required")["status"] == "ok"
    assert transition_controlled_live_session("armed", "ignored", trigger="kill_switch")["to_state"] == "emergency_stopped"
    assert arm_controlled_live_session(plan, confirm="")["status"] == "blocked"
    assert arm_controlled_live_session(plan, confirm=CONTROLLED_SESSION_CONFIRM)["status"] == "ok"

    assert evaluate_micro_position_scaling(1, 2, prior_sessions_ok=True, unreconciled_orders=0, recent_emergency_stop=False, approved=True)["status"] == "approved"
    assert evaluate_micro_position_scaling(1, 3, prior_sessions_ok=True, unreconciled_orders=0, recent_emergency_stop=False, approved=True)["status"] == "blocked"
    assert evaluate_live_session_budget(plan, {"orders": 0, "quote_exposure": 5, "single_order_quote": 5, "session_loss_quote": 0, "spread_bps": 5, "data_age_ms": 100})["decision"] == "allow"
    assert evaluate_live_session_budget(plan, {"orders": 2, "quote_exposure": 5, "single_order_quote": 5, "session_loss_quote": 0, "spread_bps": 5, "data_age_ms": 100})["decision"] == "disarm"

    assert transition_live_order_lifecycle("preview_created", "preview_validated")["status"] == "ok"
    assert transition_live_order_lifecycle("submitted", "unknown")["disarm_required"] is True
    assert reconcile_live_order({"order_id": "1", "status": "FILLED", "executed_qty": 1}, {"order_id": "1", "status": "FILLED", "executed_qty": 1})["next_order_allowed"] is True
    assert reconcile_live_order({"order_id": "1", "status": "FILLED", "executed_qty": 1}, {"order_id": "2", "status": "FILLED", "executed_qty": 1})["disarm_required"] is True
    assert live_monitoring_heartbeat(market_data_fresh=False)["disarm_required"] is True
    assert evaluate_automatic_disarm(["reconciliation_mismatch"])["status"] == "disarm"
    assert evaluate_live_circuit_breakers(["reconciliation"])["action"] == "disarm"


def test_controlled_executor_blocks_until_reconciliation_and_exports_evidence(tmp_path) -> None:
    plan = validate_live_session_plan(LiveSessionPlan())
    roadmap_118 = run_live_safety_pipeline(tmp_path)
    context = {
        "session_state": "armed",
        "plan": plan,
        "roadmap_118_context": {**roadmap_118, "arm_token": roadmap_118["arm_token"]},
        "reconciliation_required": True,
    }
    blocked = execute_controlled_live_order(context, {"orders": 0, "quote_exposure": 5, "single_order_quote": 5, "session_loss_quote": 0, "spread_bps": 5, "data_age_ms": 100}, confirm=CONTROLLED_ORDER_CONFIRM)
    assert blocked["status"] == "blocked"
    assert "next order blocked until reconciliation" in blocked["blockers"]

    context["reconciliation_required"] = False
    ok = execute_controlled_live_order(context, {"orders": 0, "quote_exposure": 5, "single_order_quote": 5, "session_loss_quote": 0, "spread_bps": 5, "data_age_ms": 100}, confirm=CONTROLLED_ORDER_CONFIRM)
    assert ok["status"] == "ok"
    assert ok["fake_live_order_submitted"] is True
    assert ok["live_order_submitted"] is False

    evidence = export_live_session_evidence(tmp_path, {"run_id": "acceptance", "executor": ok})
    assert evidence["manifest"]["no_unattended_live_proof"] is True


def test_live_session_pipeline_cli_surface_and_dashboard_api_smoke(tmp_path) -> None:
    pipeline = run_controlled_live_session_pipeline(tmp_path)
    assert pipeline["status"] == "ok"
    assert pipeline["executor"]["status"] == "blocked"
    assert pipeline["live_trading_enabled"] is False

    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    from binance_spot_bot.dashboard_v2.app import create_dashboard_v2_app

    client = TestClient(create_dashboard_v2_app())
    assert client.get("/api/live-session/status").json()["status"] == "locked"
    assert client.get("/api/live-session/budget").json()["decision"] == "allow"
    assert client.post("/api/live-session/orders/execute").json()["status"] == "blocked"
