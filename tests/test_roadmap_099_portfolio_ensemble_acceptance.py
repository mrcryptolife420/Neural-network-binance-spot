from __future__ import annotations

import json

from binance_spot_bot.allocation_policy import allocation_policy
from binance_spot_bot.champion_challenger import champion_challenger
from binance_spot_bot.ensemble_config import EnsembleConfig, EnsembleMember, validate_ensemble_config
from binance_spot_bot.ensemble_prediction import ensemble_prediction
from binance_spot_bot.portfolio_attribution import performance_attribution
from binance_spot_bot.portfolio_rotation_evidence import write_rotation_evidence
from binance_spot_bot.rotation_governance import rotation_governance
from binance_spot_bot.strategy_rotation import strategy_rotation


def test_ensemble_config_blocks_live_alias_and_weak_health() -> None:
    ok = validate_ensemble_config(EnsembleConfig("paper", [EnsembleMember("candidate", 0.4), EnsembleMember("champion_paper", 0.4)]))
    live = validate_ensemble_config(EnsembleConfig("bad", [EnsembleMember("champion_live", 0.4)]))
    weak = validate_ensemble_config(EnsembleConfig("weak", [EnsembleMember("candidate", 0.4, health_score=40)]))

    assert ok["status"] == "ok"
    assert live["status"] == "blocked"
    assert "forbidden_live_alias" in live["blockers"]
    assert "member_health_blocks_allocation" in weak["blockers"]
    assert ok["live_trading_enabled"] is False


def test_weighted_ensemble_prediction_and_allocation_policy() -> None:
    prediction = ensemble_prediction([
        {"signal": "BUY", "confidence": 0.8, "weight": 0.6},
        {"signal": "HOLD", "confidence": 0.5, "weight": 0.4},
    ])
    allowed = allocation_policy({"candidate": 0.4, "champion_paper": 0.4}, health={"candidate": 80})
    blocked = allocation_policy({"candidate": 0.7}, health={"candidate": 40})

    assert prediction["payload"]["signal"] == "BUY"
    assert allowed["status"] == "ok"
    assert blocked["status"] == "blocked"
    assert "member_health_blocks_allocation" in blocked["blockers"]


def test_rotation_governance_requires_evidence_and_blocks_live_alias() -> None:
    approved = rotation_governance(0.7, True, target_alias="candidate", evidence={"score": 0.7})
    missing_evidence = rotation_governance(0.7, True, target_alias="candidate")
    live = rotation_governance(0.8, True, target_alias="live_portfolio", evidence={"score": 0.8})

    assert approved["status"] == "approved"
    assert missing_evidence["status"] == "blocked"
    assert "evidence_required" in missing_evidence["blockers"]
    assert "live_alias_forbidden" in live["blockers"]
    assert approved["live_trading_enabled"] is False


def test_strategy_rotation_attribution_and_evidence_are_paper_only(tmp_path) -> None:
    rotation = strategy_rotation({"mean_reversion": 0.4, "trend": 0.8})
    attribution = performance_attribution([
        {"model_alias": "candidate", "symbol": "BTCUSDT", "pnl": 1.2},
        {"model_alias": "candidate", "symbol": "BTCUSDT", "pnl": -0.2},
    ])
    evidence = write_rotation_evidence(tmp_path / "rotation.json", {"rotation": rotation, "api_secret": "abcdefghijklmnopqrstuvwxyz"})
    payload = json.loads(evidence.read_text(encoding="utf-8"))

    assert rotation["selected"] == "trend"
    assert rotation["action"] == "rotate"
    assert attribution["attribution"]["candidate::BTCUSDT"]["pnl"] == 1.0
    assert payload["live_trading_enabled"] is False
    assert "[REDACTED]" in evidence.read_text(encoding="utf-8")


def test_champion_challenger_remains_paper_scope() -> None:
    result = champion_challenger(0.5, 0.8, min_delta=0.05)

    assert result["decision"] == "promote_challenger"
    assert result["scope"] == "paper_shadow_demo_only"
    assert result["live_trading_enabled"] is False
