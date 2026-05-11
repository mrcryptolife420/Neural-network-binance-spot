from __future__ import annotations

from binance_spot_bot.allocation_policy import allocation_policy
from binance_spot_bot.champion_challenger import champion_challenger
from binance_spot_bot.ensemble_prediction import ensemble_prediction
from binance_spot_bot.evidence_gap_detector import evidence_gap_detector
from binance_spot_bot.feature_drift import feature_drift
from binance_spot_bot.model_downgrade_executor import model_downgrade_executor
from binance_spot_bot.model_downgrade_policy import model_downgrade_policy
from binance_spot_bot.model_health_score import model_health_score
from binance_spot_bot.model_promotion_gate import model_promotion_gate
from binance_spot_bot.no_live_proof_pack import no_live_proof_pack
from binance_spot_bot.operator_certification import operator_certification
from binance_spot_bot.operator_glossary import operator_glossary
from binance_spot_bot.operator_signoff import operator_signoff
from binance_spot_bot.paper_os_simulation import paper_os_simulation
from binance_spot_bot.production_readiness_simulation import production_readiness_simulation
from binance_spot_bot.stabilization_gate import stabilization_gate
from binance_spot_bot.training_data_gate import training_data_gate
from binance_spot_bot.training_pipeline import run_training_pipeline


def test_097_training_pipeline_and_promotion_gate_are_contract_gated():
    blocked = training_data_gate(0, leakage_pass=True)
    trained = run_training_pipeline(10)
    promotion = model_promotion_gate(0.7, operator_confirmed=True)
    comparison = champion_challenger(0.5, 0.8)

    assert blocked["status"] == "blocked"
    assert trained["gate"]["status"] == "ok"
    assert promotion["status"] == "ok"
    assert comparison["decision"] == "promote_challenger"


def test_098_monitoring_detects_drift_and_requires_confirmed_downgrade():
    drift = feature_drift([1, 2, 3], [1, 1, 1])
    health = model_health_score(0.4, performance_ok=True)
    policy = model_downgrade_policy(health["score"])
    blocked = model_downgrade_executor(policy["action"], confirm="")

    assert drift["payload"]["status"] == "warn"
    assert health["status"] == "warn"
    assert policy["action"] == "downgrade_candidate"
    assert blocked["status"] == "blocked"


def test_099_ensemble_allocation_and_prediction_are_paper_only():
    allocation = allocation_policy({"a": 0.4, "b": 0.4})
    prediction = ensemble_prediction([{"signal": "BUY", "confidence": 0.8}, {"signal": "BUY", "confidence": 0.6}])

    assert allocation["status"] == "ok"
    assert prediction["payload"]["signal"] == "BUY"
    assert prediction["live_trading_enabled"] is False


def test_100_paper_os_audit_blocks_production_readiness():
    sim = paper_os_simulation()
    readiness = production_readiness_simulation()
    proof = no_live_proof_pack()
    signoff = operator_signoff("PAPER_OS_SIGNOFF")

    assert sim["payload"]["status"] == "ready"
    assert readiness["status"] == "blocked"
    assert proof["signed_endpoints_used"] is False
    assert signoff["status"] == "signed"


def test_101_stabilization_gate_burns_down_unwaived_blockers():
    blocked = stabilization_gate(["slow_check", "missing_evidence"], ["slow_check"])
    ok = stabilization_gate(["slow_check"], ["slow_check"])
    gaps = evidence_gap_detector(["a", "b"], ["a"])

    assert blocked["status"] == "blocked"
    assert ok["status"] == "ok"
    assert gaps["missing"] == ["b"]


def test_102_operator_training_and_manual_surfaces():
    glossary = operator_glossary()
    failed = operator_certification(60)
    passed = operator_certification(90)

    assert glossary["terms"]["live"] == "disabled"
    assert failed["status"] == "failed"
    assert passed["status"] == "passed"
    assert passed["live_trading_enabled"] is False
