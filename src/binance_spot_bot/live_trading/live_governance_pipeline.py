from __future__ import annotations

from pathlib import Path
from typing import Any

from .live_execution_quality import analyze_live_execution_quality
from .live_governance_evidence import export_live_governance_evidence
from .live_profile_lifecycle import apply_live_profile_lifecycle
from .live_session_regression import compare_live_session_regression
from .live_session_review import fixture_review_input, run_live_session_review, write_live_session_review_report
from .live_session_scorecards import generate_live_session_scorecard
from .operator_approval_workflow import create_operator_approval_request, decide_operator_approval
from .risk_limit_calibration import calibrate_live_risk_limits
from .risk_preset_proposals import build_risk_preset_proposal
from .scaling_governance import decide_live_scaling


def run_live_governance_pipeline(root: Path, *, approval_confirm: str = "", approval_note: str = "") -> dict[str, Any]:
    review = run_live_session_review(fixture_review_input())
    write_live_session_review_report(root, review)
    scorecard = generate_live_session_scorecard(review, {"slippage_bps": 5, "unreconciled_orders": 0})
    execution_quality = analyze_live_execution_quality({"preview_price": 100, "execution_price": 100.05, "fee_quote": 0.01})
    calibration = calibrate_live_risk_limits(scorecard, {"max_single_order_quote": 5, "max_session_exposure": 15, "max_session_orders": 2})
    scaling = decide_live_scaling(1, 2, scorecard, approved=bool(approval_confirm), successful_sessions=1)
    approval_request = create_operator_approval_request("approve_next_level", "live-session-evidence-fixture")
    approval = decide_operator_approval(approval_request, confirm=approval_confirm, note=approval_note)
    lifecycle = apply_live_profile_lifecycle("controlled_level_1", "promote", approved=approval["status"] == "approved", blocker=scaling["status"] != "ok")
    risk_proposal = build_risk_preset_proposal("keep_same", {"max_single_order_quote": 5, "max_session_exposure": 15})
    regression = compare_live_session_regression({"slippage_bps": 5}, {"slippage_bps": 10})
    evidence = export_live_governance_evidence(root, {"run_id": "live-governance-pipeline", "review": review, "scorecard": scorecard, "calibration": calibration, "scaling": scaling, "approval": approval, "lifecycle": lifecycle, "live_trading_enabled": False})
    return {"status": "ok", "review": review, "scorecard": scorecard, "execution_quality": execution_quality, "calibration": calibration, "scaling": scaling, "approval_request": approval_request, "approval": approval, "lifecycle": lifecycle, "risk_proposal": risk_proposal, "regression": regression, "evidence": evidence, "live_order_submitted": False, "live_trading_enabled": False}
