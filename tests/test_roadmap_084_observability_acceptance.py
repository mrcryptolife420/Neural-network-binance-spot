from __future__ import annotations

import json
import time

from binance_spot_bot.governance_metrics import governance_metric_snapshot
from binance_spot_bot.local_ops_metrics import local_ops_metric_snapshot
from binance_spot_bot.long_term_analytics_report import write_long_term_analytics_report
from binance_spot_bot.metrics_aggregation import aggregate_daily_metrics, aggregate_weekly_metrics
from binance_spot_bot.metrics_anomaly_detection import detect_metric_anomalies
from binance_spot_bot.metrics_collectors import collect_artifact_metrics, collect_dashboard_smoke_metrics, missing_artifact_metric
from binance_spot_bot.metrics_evidence_bundle import export_metrics_evidence_bundle, verify_metrics_evidence_bundle
from binance_spot_bot.metrics_retention import metrics_retention_plan
from binance_spot_bot.metrics_schema import MetricEvent
from binance_spot_bot.metrics_warehouse import MetricsWarehouse, write_metrics_report
from binance_spot_bot.ops_slo import evaluate_ops_slo
from binance_spot_bot.paper_performance_metrics import paper_performance_summary


def test_metric_event_redacts_labels_and_rejects_live():
    event = MetricEvent("operator.health", 1.0, labels={"api_key": "placeholder"}, category="health")
    payload = event.to_dict()

    assert payload["labels"]["api_key"] == "[REDACTED]"
    assert payload["schema_version"] == "1.0"
    assert payload["live_trading_enabled"] is False


def test_metrics_warehouse_append_query_latest_manifest_and_compaction(tmp_path):
    warehouse = MetricsWarehouse(tmp_path / "metrics")
    first = MetricEvent("operator.health", 1.0, source="test", category="health")
    second = MetricEvent("paper.pnl", -2.0, source="test", category="paper_performance", unit="quote")

    warehouse.append_metric(first)
    warehouse.append_many([second])
    manifest = warehouse.write_manifest()

    assert warehouse.latest_metric("operator.health")["value"] == 1.0
    assert len(warehouse.query_metrics(category="paper_performance")) == 1
    assert warehouse.verify_manifest(manifest)["status"] == "ok"
    assert warehouse.compact_old_metrics(keep_latest=1)["status"] == "preview"
    assert warehouse.compact_old_metrics(keep_latest=1, confirm="COMPACT_METRICS")["status"] == "compacted"


def test_collectors_local_ops_paper_and_governance_metrics(tmp_path):
    smoke = tmp_path / "browser-smoke.json"
    smoke.write_text(json.dumps({"status": "ok", "checks": [{"status": "ok"}]}), encoding="utf-8")

    artifact = collect_artifact_metrics([{"bytes": 10}, {"bytes": 20}])
    dashboard = collect_dashboard_smoke_metrics(smoke)
    missing = missing_artifact_metric("evidence.missing", tmp_path / "missing.json")
    local_ops = local_ops_metric_snapshot([{"job_id": "a"}], [{"status": "failed"}])
    paper = paper_performance_summary([{"pnl": "1.5", "drawdown": "2", "fills": 3}])
    governance = governance_metric_snapshot([{"decision": "promote_challenger"}, {"decision": "rollback"}], [{"status": "suspended"}])

    assert artifact["artifact_count"] == 2
    assert dashboard[0].name == "dashboard.smoke_status"
    assert missing.status == "missing"
    assert local_ops["status"] == "warn"
    assert paper["pnl"] == 1.5
    assert governance["status"] == "warn"


def test_aggregation_slo_anomalies_reports_retention_and_bundle(tmp_path):
    rows = [
        MetricEvent("check_all.success", 1.0, category="check").to_dict(),
        MetricEvent("paper.pnl", -5.0, category="paper_performance").to_dict(),
        {"name": "old.metric", "value": 1, "timestamp_ms": int(time.time() * 1000) - 90_000_000},
        {"name": "job.status", "value": 0, "status": "failed", "timestamp_ms": int(time.time() * 1000)},
        {"name": "job.status", "value": 0, "status": "failed", "timestamp_ms": int(time.time() * 1000)},
    ]
    daily = aggregate_daily_metrics(rows, tmp_path / "daily.json")
    weekly = aggregate_weekly_metrics(rows, tmp_path / "weekly.json")
    slo = evaluate_ops_slo({"check_all_success_rate": 0.5, "dashboard_smoke_success_rate": 1.0, "live_trading_enabled": False})
    anomalies = detect_metric_anomalies(rows)
    report_paths = write_long_term_analytics_report(tmp_path, {"status": "warn", "recommended_action": "review"})
    retention = metrics_retention_plan(rows, keep_latest=2)
    bundle = export_metrics_evidence_bundle([tmp_path / "daily.json", tmp_path / "weekly.json", report_paths["json"]], tmp_path / "bundle")

    assert daily["path"].endswith("daily.json")
    assert weekly["period"] == "weekly"
    assert slo["status"] == "breach"
    assert anomalies["status"] == "warn"
    assert report_paths["json"]
    assert retention["status"] == "preview"
    assert verify_metrics_evidence_bundle(bundle["manifest"])["status"] == "ok"
    assert bundle["live_trading_enabled"] is False


def test_write_metrics_report_keeps_existing_cli_surface(tmp_path):
    settings = type("S", (), {"data_dir": tmp_path})()
    report = write_metrics_report(settings, [{"equity": 1000, "pnl_quote": 1.25}, {"equity": 1001, "pnl_quote": -0.5}])

    assert report["rows"] >= 2
    assert report["paths"]["json"].endswith("latest-metrics-report.json")
    assert report["live_trading_enabled"] is False
