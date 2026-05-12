from __future__ import annotations

import json
from pathlib import Path

from binance_spot_bot.backup_preflight import backup_preflight
from binance_spot_bot.backup_profiles import backup_profiles, default_backup_profiles, validate_backup_profile
from binance_spot_bot.backup_verification import verify_backup
from binance_spot_bot.data_dir_migration import data_dir_migration_preview
from binance_spot_bot.disaster_recovery_report import write_disaster_recovery_report
from binance_spot_bot.dr_evidence_bundle import export_dr_evidence_bundle, verify_dr_evidence_bundle
from binance_spot_bot.evidence_continuity import evidence_continuity_check
from binance_spot_bot.offline_backup import create_offline_backup
from binance_spot_bot.permission_restore_validation import permission_restore_validate
from binance_spot_bot.restore_drill import restore_drill
from binance_spot_bot.restore_executor import restore_execute
from binance_spot_bot.restore_preview import restore_preview
from binance_spot_bot.state_integrity import state_integrity_check
from binance_spot_bot.state_inventory import state_inventory, write_state_inventory


def _fixture(root: Path) -> None:
    (root / "reports").mkdir(parents=True)
    (root / "reports" / "report.json").write_text(json.dumps({"ok": True, "live_trading_enabled": False}), encoding="utf-8")
    (root / "action-center").mkdir()
    (root / "action-center" / "decision-journal.jsonl").write_text(json.dumps({"decision": "approve"}) + "\n", encoding="utf-8")
    (root / ".env").write_text("BINANCE_API_SECRET=blocked", encoding="utf-8")
    (root / "key.pem").write_text("blocked", encoding="utf-8")


def test_backup_profiles_inventory_preflight_and_package_are_secret_free(tmp_path: Path) -> None:
    _fixture(tmp_path)
    profiles = backup_profiles()
    inventory = state_inventory(tmp_path)
    preflight = backup_preflight(tmp_path, profile_id="paper_ops_full")
    backup = create_offline_backup(tmp_path, tmp_path / "backup.zip", profile_id="paper_ops_full")
    verify = verify_backup(Path(backup["zip"]))

    assert profiles["status"] == "ready"
    assert validate_backup_profile(default_backup_profiles()["paper_ops_full"]).allowed is True
    assert any(item["path"] == ".env" and item["include_eligible"] is False for item in inventory["items"])
    assert any(item["path"] == "key.pem" and item["include_eligible"] is False for item in inventory["items"])
    assert preflight["status"] == "blocked"
    assert verify["status"] == "ok"
    assert ".env" not in " ".join(item["path"] for item in verify["files"])
    assert backup["live_trading_enabled"] is False


def test_restore_preview_drill_executor_integrity_and_continuity(tmp_path: Path) -> None:
    _fixture(tmp_path)
    backup = create_offline_backup(tmp_path, tmp_path / "backup.zip", profile_id="paper_ops_full")
    target = tmp_path / "restore-target"
    preview = restore_preview(Path(backup["zip"]), target)
    drill = restore_drill(Path(backup["zip"]))
    blocked_restore = restore_execute(Path(backup["zip"]), target, confirm="", mode="restore")
    restored = restore_execute(Path(backup["zip"]), target, confirm="RESTORE_OFFLINE_STATE", mode="restore")
    integrity = state_integrity_check(target)
    permission = permission_restore_validate(target)
    continuity = evidence_continuity_check(Path(backup["zip"]), target)

    assert preview["preview_only"] is True
    assert ".env" not in preview["creates"]
    assert drill["status"] == "pass"
    assert blocked_restore["status"] == "blocked"
    assert restored["status"] == "ok"
    assert integrity["status"] in {"ok", "warn"}
    assert permission["live_trading_enabled"] is False
    assert continuity["status"] in {"ok", "warn"}


def test_reports_bundle_migration_and_corrupt_detection(tmp_path: Path) -> None:
    _fixture(tmp_path)
    backup = create_offline_backup(tmp_path, tmp_path / "backup.zip", profile_id="paper_ops_full")
    corrupt = tmp_path / "reports" / "corrupt.json"
    corrupt.write_text("{", encoding="utf-8")
    inventory = write_state_inventory(tmp_path)
    integrity = state_integrity_check(tmp_path)
    report = write_disaster_recovery_report(tmp_path, {"status": "ok", "backup": backup, "integrity": integrity})
    bundle = export_dr_evidence_bundle(tmp_path, [Path(report["path"]), Path(inventory["path"])])
    verified = verify_dr_evidence_bundle(Path(bundle["manifest"]))
    migration = data_dir_migration_preview(tmp_path, tmp_path / "new-data")

    assert integrity["status"] in {"warn", "blocked"}
    assert any(item["reason"] == "invalid_json" for item in integrity["issues"])
    assert report["no_live_proof"] is True
    assert bundle["redaction_proof"] is True
    assert verified["status"] == "ok"
    assert migration["preview_only"] is True
