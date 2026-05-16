from __future__ import annotations

import json

from binance_spot_bot.live_trading import LIVE_RISK_CONFIRM, REAL_ORDER_CONFIRM
from binance_spot_bot.live_trading.first_live_order_gate import evaluate_first_live_order_gate
from binance_spot_bot.live_trading.live_account_verifier import FakeLiveReadOnlyAdapter, verify_live_read_only_account
from binance_spot_bot.live_trading.live_arm_token import create_live_arm_token, validate_live_arm_token
from binance_spot_bot.live_trading.live_audit import append_live_audit_event, verify_live_audit_chain
from binance_spot_bot.live_trading.live_dry_run_session import run_live_dry_run_session
from binance_spot_bot.live_trading.live_endpoint_policy import endpoint_allowed, live_endpoint_policy_report
from binance_spot_bot.live_trading.live_evidence_prerequisite_gate import evaluate_live_evidence_prerequisites, fixture_live_evidence
from binance_spot_bot.live_trading.live_execution_adapter import FakeFirstOrderAdapter, execute_first_order_with_adapter
from binance_spot_bot.live_trading.live_execution_evidence import export_live_execution_evidence
from binance_spot_bot.live_trading.live_order_preview import build_live_order_preview
from binance_spot_bot.live_trading.live_order_sizing_guard import evaluate_live_order_sizing
from binance_spot_bot.live_trading.live_safety_drills import run_live_cancel_drill, run_live_kill_switch_drill
from binance_spot_bot.live_trading.live_safety_pipeline import run_live_safety_pipeline
from binance_spot_bot.live_trading.live_session_state import transition_live_session


def _context() -> dict:
    evidence = evaluate_live_evidence_prerequisites(fixture_live_evidence())
    account = verify_live_read_only_account()
    dry_run = run_live_dry_run_session(fixture_live_evidence())
    preview = build_live_order_preview({"symbol": "BTCUSDT", "side": "BUY", "quote": 5})
    sizing = evaluate_live_order_sizing(preview, max_balance_pct=0.10)
    kill = run_live_kill_switch_drill()
    cancel = run_live_cancel_drill()
    context = {"evidence": evidence, "account": account, "dry_run": dry_run, "preview": preview, "sizing": sizing, "kill_switch_drill": kill, "cancel_drill": cancel}
    context["arm_token"] = create_live_arm_token(context, confirm=LIVE_RISK_CONFIRM)
    return context


def test_live_evidence_prerequisites_block_missing_low_quality_testnet_and_secrets() -> None:
    assert evaluate_live_evidence_prerequisites({})["status"] == "blocked"
    assert evaluate_live_evidence_prerequisites(fixture_live_evidence(quality_grade="C"))["state"] == "blocked_low_quality_data"
    assert evaluate_live_evidence_prerequisites(fixture_live_evidence(validation_grade="D"))["state"] == "blocked_validation_failed"
    assert evaluate_live_evidence_prerequisites(fixture_live_evidence(testnet_ok=False))["state"] == "blocked_testnet_failed"
    secret_report = evaluate_live_evidence_prerequisites({"api_secret": "A" * 64, "manifest": {"hashes": ["x"]}})
    assert "A" * 64 not in json.dumps(secret_report)
    assert secret_report["live_execution_enabled"] is False
    assert secret_report["live_order_placement_enabled"] is False


def test_read_only_account_endpoint_policy_dry_run_preview_and_sizing() -> None:
    account = verify_live_read_only_account(FakeLiveReadOnlyAdapter())
    assert account["status"] == "ok"
    assert account["order_endpoints_called"] is False
    assert verify_live_read_only_account(FakeLiveReadOnlyAdapter(base_url="https://demo-api.binance.com/api"))["status"] == "blocked"

    assert endpoint_allowed("dry_run", "place_order") is False
    assert endpoint_allowed("first_order", "place_order", confirm=REAL_ORDER_CONFIRM) is True
    assert live_endpoint_policy_report("preview", ["get_account_state", "place_order"])["status"] == "blocked"

    dry_run = run_live_dry_run_session(fixture_live_evidence())
    assert dry_run["status"] == "ok"
    assert dry_run["place_order_called"] is False
    preview = build_live_order_preview({"symbol": "BTCUSDT", "quote": 5})
    assert preview["status"] == "preview"
    assert preview["preview_hash"]
    assert evaluate_live_order_sizing(preview, max_balance_pct=0.10)["status"] == "ok"
    assert evaluate_live_order_sizing({**preview, "quote_size": 500})["status"] == "blocked"


def test_arm_token_drills_first_order_gate_and_adapter_are_one_time(tmp_path) -> None:
    context = _context()
    assert context["arm_token"]["status"] == "ok"
    assert validate_live_arm_token(context["arm_token"])["status"] == "ok"
    assert validate_live_arm_token(context["arm_token"], consumed=True)["status"] == "blocked"
    assert run_live_kill_switch_drill()["order_path_blocked"] is True
    assert run_live_cancel_drill()["status"] == "ok"

    assert evaluate_first_live_order_gate(context, confirm="")["status"] == "blocked"
    adapter = FakeFirstOrderAdapter()
    first = evaluate_first_live_order_gate(context, confirm=REAL_ORDER_CONFIRM, adapter=adapter)
    assert first["status"] == "ok"
    assert first["adapter_place_order_calls"] == 1
    assert first["disarmed_after_order"] is True
    assert first["live_order_submitted"] is False
    assert execute_first_order_with_adapter(adapter, {"symbol": "BTCUSDT"})["status"] == "blocked"

    evidence = export_live_execution_evidence(tmp_path, {"run_id": "acceptance", "first_order": first})
    assert evidence["manifest"]["secret_redaction_proof"] is True


def test_live_session_state_audit_pipeline_and_dashboard_api_smoke(tmp_path) -> None:
    assert transition_live_session("locked", "evidence_required")["status"] == "ok"
    assert transition_live_session("ready_to_arm", "locked")["status"] == "blocked"
    assert transition_live_session("armed", "ignored", trigger="kill_switch")["to_state"] == "emergency_stopped"
    assert transition_live_session("armed", "ignored", trigger="restart")["to_state"] == "locked"

    chain: list[dict] = []
    append_live_audit_event(chain, "preview", {"api_secret": "A" * 64})
    assert verify_live_audit_chain(chain)["status"] == "ok"
    assert "A" * 64 not in json.dumps(chain)

    pipeline = run_live_safety_pipeline(tmp_path)
    assert pipeline["status"] == "ok"
    assert pipeline["first_order"]["status"] == "blocked"
    assert pipeline["live_trading_enabled"] is False

    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    from binance_spot_bot.dashboard_v2.app import create_dashboard_v2_app

    client = TestClient(create_dashboard_v2_app())
    assert client.get("/api/live/status").json()["status"] == "locked"
    assert client.post("/api/live/dry-run/start").json()["place_order_called"] is False
    assert client.post("/api/live/first-order/execute").json()["status"] == "blocked"
