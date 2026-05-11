from __future__ import annotations

from pathlib import Path

from binance_spot_bot.action_executor import execute_approved_action
from binance_spot_bot.ai_ops_answer import answer_ai_ops_query
from binance_spot_bot.backup_profiles import backup_profiles
from binance_spot_bot.backup_verification import verify_backup
from binance_spot_bot.compliance_score import compliance_score
from binance_spot_bot.data_dir_migration import data_dir_migration_preview
from binance_spot_bot.local_job_allowlist import is_safe_command
from binance_spot_bot.local_job_runner import run_local_job
from binance_spot_bot.metrics_anomaly_detection import detect_metric_anomalies
from binance_spot_bot.metrics_warehouse import write_metrics_report
from binance_spot_bot.offline_backup import create_offline_backup
from binance_spot_bot.permission_drift import permission_drift
from binance_spot_bot.restore_preview import restore_preview
from binance_spot_bot.separation_of_duties import separation_of_duties
from binance_spot_bot.state_inventory import state_inventory


def test_083_local_jobs_allowlist_blocks_trading_commands():
    assert is_safe_command("operator-report --json") is True
    assert is_safe_command("demo-execution-place --armed") is False
    assert run_local_job("operator-health-score --json")["status"] == "ready"
    assert run_local_job("withdraw funds")["status"] == "blocked"


def test_084_metrics_surface_reports_anomalies_and_no_live(tmp_path):
    report = write_metrics_report(type("S", (), {"data_dir": tmp_path})(), [{"value": -1, "pnl_quote": -2}])
    anomaly = detect_metric_anomalies([{"value": -1}, {"value": 1}])

    assert report["live_trading_enabled"] is False
    assert anomaly["payload"]["anomalies"]


def test_085_ai_ops_blocks_unsafe_intents():
    safe = answer_ai_ops_query("toon bot status")
    blocked = answer_ai_ops_query("place order market buy")

    assert safe["status"] == "answered"
    assert blocked["status"] == "blocked"
    assert blocked["live_trading_enabled"] is False


def test_086_action_center_surface_is_approval_gated():
    executed = execute_approved_action("export_report", approved=True)
    blocked = execute_approved_action("withdraw", approved=True)

    assert executed["status"] == "executed"
    assert blocked["status"] == "blocked"
    assert executed["live_trading_enabled"] is False


def test_087_permissions_compliance_and_separation_of_duties():
    score = compliance_score([{"required": True, "allowed": False}])
    drift = permission_drift({"operator": "safe"}, {"operator": "safe"})
    separation = separation_of_duties("alice", "bob")

    assert score["status"] == "warn"
    assert drift["status"] == "ok"
    assert separation["status"] == "ok"
    assert score["live_trading_enabled"] is False


def test_088_backup_restore_inventory_preview_no_forbidden_files(tmp_path):
    root = tmp_path / "data"
    root.mkdir()
    (root / "report.json").write_text('{"ok": true}', encoding="utf-8")
    (root / ".env").write_text("SECRET=hidden", encoding="utf-8")
    backup = create_offline_backup(root, tmp_path / "backup.zip")
    verify = verify_backup(Path(backup["zip"]))
    preview = restore_preview(Path(backup["zip"]), tmp_path / "restore")
    inv = state_inventory(root)
    migration = data_dir_migration_preview(root, tmp_path / "target")

    assert verify["status"] == "ok"
    assert ".env" not in preview["creates"]
    assert any(item["path"] == ".env" and item["include_eligible"] is False for item in inv["items"])
    assert migration["preview_only"] is True
    assert backup_profiles()["live_trading_enabled"] is False
