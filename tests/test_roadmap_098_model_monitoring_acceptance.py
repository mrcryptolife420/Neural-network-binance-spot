from __future__ import annotations

from binance_spot_bot.feature_drift import feature_drift
from binance_spot_bot.model_downgrade_executor import model_downgrade_executor
from binance_spot_bot.model_downgrade_policy import model_downgrade_policy
from binance_spot_bot.model_health_score import model_health_score
from binance_spot_bot.model_monitoring_config import ModelMonitoringConfig, ModelMonitoringScope, validate_model_monitoring_config
from binance_spot_bot.model_monitoring_pipeline import run_model_monitoring
from binance_spot_bot.paper_performance_monitor import paper_performance_monitor
from binance_spot_bot.prediction_drift import confidence_drift, prediction_drift
from binance_spot_bot.shadow_prediction_logger import log_shadow_prediction


def test_monitoring_config_blocks_live_aliases() -> None:
    ok = validate_model_monitoring_config(ModelMonitoringConfig())
    blocked = validate_model_monitoring_config(ModelMonitoringConfig(scope=ModelMonitoringScope(monitored_aliases=["champion_live"])))

    assert ok["status"] == "ok"
    assert blocked["status"] == "blocked"
    assert "forbidden_live_alias_in_scope" in blocked["blockers"]
    assert blocked["live_trading_enabled"] is False


def test_shadow_prediction_logging_is_local_redacted_and_no_execution(tmp_path) -> None:
    path = tmp_path / "shadow" / "predictions.jsonl"
    result = log_shadow_prediction(
        path,
        model_alias="candidate",
        symbol="BTCUSDT",
        prediction={"signal": "BUY", "confidence": 0.7},
        features={"api_secret": "abcdefghijklmnopqrstuvwxyz"},
    )

    assert result["status"] == "ok"
    assert "[REDACTED]" in path.read_text(encoding="utf-8")
    assert result["live_trading_enabled"] is False


def test_drift_performance_health_and_policy_pipeline() -> None:
    fd = feature_drift([1, 2, 3], [1, 1, 1])
    pd = prediction_drift([0.1, 0.2], [0.8, 0.9])
    cd = confidence_drift([0.5, 0.5], [0.9, 0.9])
    perf = paper_performance_monitor([{"pnl": -20, "drawdown": 30}])
    health = model_health_score(max(fd["payload"]["score"], pd["payload"]["score"], cd["payload"]["score"]), performance_ok=perf["status"] == "ok")
    policy = model_downgrade_policy(health["score"])

    assert fd["payload"]["status"] == "warn"
    assert pd["status"] == "warn"
    assert cd["status"] == "warn"
    assert perf["status"] == "warn"
    assert health["status"] in {"warn", "blocked"}
    assert policy["action"] == "downgrade_candidate"


def test_downgrade_executor_blocks_live_alias_and_requires_evidence(tmp_path) -> None:
    blocked_confirm = model_downgrade_executor("downgrade_candidate", "", root=tmp_path, evidence={"reason": "drift"})
    blocked_live = model_downgrade_executor("downgrade_candidate", "DOWNGRADE_PAPER_MODEL", alias="champion_live", root=tmp_path, evidence={"reason": "drift"})
    applied = model_downgrade_executor("downgrade_candidate", "DOWNGRADE_PAPER_MODEL", alias="candidate", root=tmp_path, evidence={"reason": "drift"})

    assert blocked_confirm["status"] == "blocked"
    assert blocked_live["status"] == "blocked"
    assert "alias_not_allowed_for_downgrade" in blocked_live["blockers"]
    assert applied["status"] == "applied"
    assert (tmp_path / "model-monitoring" / "alias-history.jsonl").exists()
    assert applied["live_trading_enabled"] is False


def test_model_monitoring_pipeline_recommends_safe_downgrade() -> None:
    payload = run_model_monitoring(
        baseline_features=[1, 1, 1],
        current_features=[2, 2, 2],
        reference_predictions=[0.1, 0.2, 0.1],
        current_predictions=[0.8, 0.9, 0.85],
        reference_confidence=[0.5, 0.5, 0.5],
        current_confidence=[0.95, 0.95, 0.95],
        paper_rows=[{"pnl": -20, "drawdown": 30}],
    )

    assert payload["status"] == "ok"
    assert payload["downgrade_policy"]["action"] == "downgrade_candidate"
    assert payload["live_trading_enabled"] is False
