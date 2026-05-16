from __future__ import annotations

import json

from binance_spot_bot.live_trading import LIVE_SCALING_APPROVAL_CONFIRM
from binance_spot_bot.live_trading.live_execution_quality import analyze_live_execution_quality
from binance_spot_bot.live_trading.live_governance_pipeline import run_live_governance_pipeline
from binance_spot_bot.live_trading.live_profile_lifecycle import apply_live_profile_lifecycle
from binance_spot_bot.live_trading.live_session_regression import compare_live_session_regression
from binance_spot_bot.live_trading.live_session_review import fixture_review_input, run_live_session_review
from binance_spot_bot.live_trading.live_session_scorecards import generate_live_session_scorecard
from binance_spot_bot.live_trading.operator_approval_workflow import create_operator_approval_request, decide_operator_approval
from binance_spot_bot.live_trading.risk_limit_calibration import calibrate_live_risk_limits
from binance_spot_bot.live_trading.risk_preset_proposals import build_risk_preset_proposal
from binance_spot_bot.live_trading.scaling_governance import decide_live_scaling


def test_review_blocks_missing_evidence_unknown_unreconciled_hash_and_redacts() -> None:
    valid = run_live_session_review(fixture_review_input())
    assert valid["status"] == "ok"
    assert valid["eligible_for_scorecard"] is True
    assert valid["eligible_for_scaling_review"] is False
    assert "NO AUTOMATIC LIVE SCALE-UP" in valid["no_auto_scale_statement"]

    missing = run_live_session_review({})
    assert "missing live session evidence manifest" in missing["blockers"]
    unknown = run_live_session_review({**fixture_review_input(), "order_states": ["unknown"]})
    assert "unknown order state" in unknown["blockers"]
    unreconciled = run_live_session_review({**fixture_review_input(), "order_states": ["unreconciled"]})
    assert "unreconciled order" in unreconciled["blockers"]
    hash_fail = run_live_session_review({**fixture_review_input(), "evidence_hash_ok": False})
    assert "evidence hash mismatch" in hash_fail["blockers"]
    unsafe = "A" * 64
    redacted = run_live_session_review({**fixture_review_input(), "operator_notes": unsafe})
    assert unsafe not in json.dumps(redacted)


def test_scorecard_execution_quality_calibration_scaling_and_approval() -> None:
    review = run_live_session_review(fixture_review_input())
    scorecard = generate_live_session_scorecard(review, {"slippage_bps": 5})
    assert scorecard["grade"] == "A"
    assert scorecard["eligible_for_scaling_review"] is True
    assert analyze_live_execution_quality({"preview_price": 100, "execution_price": 101, "max_slippage_bps": 25})["status"] == "blocked"

    calibration = calibrate_live_risk_limits(scorecard, {"max_single_order_quote": 5, "max_session_exposure": 15, "max_session_orders": 2})
    assert calibration["mutates_active_profile"] is False
    blocked_scaling = decide_live_scaling(1, 2, scorecard, approved=False, successful_sessions=1)
    assert "operator approval required" in blocked_scaling["blockers"]
    approved_scaling = decide_live_scaling(1, 2, scorecard, approved=True, successful_sessions=1)
    assert approved_scaling["decision"] == "approved_for_next_level"

    request = create_operator_approval_request("approve_next_level", "evidence-fixture")
    assert decide_operator_approval(request, confirm="", note="ok")["status"] == "blocked"
    assert decide_operator_approval(request, confirm=LIVE_SCALING_APPROVAL_CONFIRM, note="reviewed")["status"] == "approved"


def test_profile_lifecycle_proposals_regression_and_pipeline(tmp_path) -> None:
    assert apply_live_profile_lifecycle("controlled_level_1", "promote", approved=False)["status"] == "blocked"
    assert apply_live_profile_lifecycle("controlled_level_1", "promote", approved=True)["status"] == "promoted"
    proposal = build_risk_preset_proposal("reduce_order_size", {"max_single_order_quote": 5})
    assert proposal["mutates_active_profile"] is False
    assert proposal["proposed_patch"]["max_single_order_quote"] == 2.5
    assert compare_live_session_regression({"slippage_bps": 10}, {"slippage_bps": 5})["status"] == "warn"

    pipeline = run_live_governance_pipeline(tmp_path)
    assert pipeline["status"] == "ok"
    assert pipeline["live_order_submitted"] is False
    assert pipeline["scaling"]["status"] == "blocked"
    assert pipeline["evidence"]["manifest"]["no_auto_scale_proof"] is True


def test_live_governance_dashboard_api_smoke() -> None:
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    from binance_spot_bot.dashboard_v2.app import create_dashboard_v2_app

    client = TestClient(create_dashboard_v2_app())
    assert client.get("/api/live-governance/status").json()["no_auto_scale"] is True
    assert client.post("/api/live-governance/review/run").json()["status"] == "ok"
    assert client.post("/api/live-governance/scaling-decision").json()["status"] == "blocked"
