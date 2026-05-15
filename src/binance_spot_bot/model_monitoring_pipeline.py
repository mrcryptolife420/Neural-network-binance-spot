from __future__ import annotations

from pathlib import Path
from typing import Any

from .feature_drift import feature_drift
from .model_downgrade_policy import model_downgrade_policy
from .model_health_score import model_health_score
from .model_monitoring_config import ModelMonitoringConfig, validate_model_monitoring_config
from .paper_performance_monitor import paper_performance_monitor
from .prediction_drift import confidence_drift, prediction_drift


def run_model_monitoring(
    *,
    baseline_features: list[float],
    current_features: list[float],
    reference_predictions: list[float],
    current_predictions: list[float],
    reference_confidence: list[float],
    current_confidence: list[float],
    paper_rows: list[dict[str, Any]],
    config: ModelMonitoringConfig | None = None,
) -> dict[str, Any]:
    config = config or ModelMonitoringConfig()
    config_validation = validate_model_monitoring_config(config)
    fd = feature_drift(current_features, baseline_features, config.drift.feature_drift_warn)
    pd = prediction_drift(reference_predictions, current_predictions, config.drift.prediction_drift_warn)
    cd = confidence_drift(reference_confidence, current_confidence, config.drift.confidence_drift_warn)
    perf = paper_performance_monitor(
        paper_rows,
        min_pnl_quote=config.performance.min_pnl_quote,
        max_drawdown_quote=config.performance.max_drawdown_quote,
    )
    drift_score = max(fd["payload"]["score"], pd["payload"]["score"], cd["payload"]["score"])
    health = model_health_score(drift_score, performance_ok=perf["status"] == "ok")
    policy = model_downgrade_policy(health["score"], drift_status=health["status"], evidence_present=True)
    return {
        "status": "ok" if config_validation["status"] == "ok" else "blocked",
        "config_validation": config_validation,
        "feature_drift": fd,
        "prediction_drift": pd,
        "confidence_drift": cd,
        "paper_performance": perf,
        "health": health,
        "downgrade_policy": policy,
        "live_trading_enabled": False,
    }
