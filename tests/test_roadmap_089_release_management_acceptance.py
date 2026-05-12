from __future__ import annotations

from pathlib import Path

from binance_spot_bot.backup_verification import verify_backup
from binance_spot_bot.migration_apply import migration_apply
from binance_spot_bot.migration_dry_run import migration_dry_run
from binance_spot_bot.migration_registry import migration_plan, migration_registry
from binance_spot_bot.offline_backup import create_offline_backup
from binance_spot_bot.post_upgrade_validation import post_upgrade_validation
from binance_spot_bot.pre_upgrade_backup_gate import pre_upgrade_backup_gate
from binance_spot_bot.release_candidate import release_candidate
from binance_spot_bot.release_evidence_bundle import export_release_evidence_bundle, verify_release_evidence_bundle
from binance_spot_bot.release_manifest import create_release_manifest, verify_release_manifest
from binance_spot_bot.release_notes import release_notes
from binance_spot_bot.release_quality_gate import release_quality_gate
from binance_spot_bot.rollback_planner import rollback_plan
from binance_spot_bot.schema_registry import schema_registry, validate_schema_registry
from binance_spot_bot.upgrade_compatibility import upgrade_compatibility
from binance_spot_bot.versioning import build_install_fingerprint, detect_project_version, version_payload


def test_version_fingerprint_manifest_notes_and_schema(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\nversion='9.8.7'\n", encoding="utf-8")
    version = detect_project_version(tmp_path)
    fingerprint = build_install_fingerprint(tmp_path, tmp_path / "data")
    manifest = create_release_manifest(tmp_path / "data", "9.8.8", previous_version="9.8.7", migration_required=True)
    notes = release_notes("9.8.8", ["release safety"], root=tmp_path / "data")
    schemas = schema_registry()

    assert version.version == "9.8.7"
    assert fingerprint["payload"]["live_trading_enabled"] is False
    assert verify_release_manifest(manifest)["status"] == "ok"
    assert manifest["migration"]["pre_upgrade_backup_required"] is True
    assert notes["backup_required"] is True
    assert schemas["status"] == "ok"
    assert validate_schema_registry({"unknown": "1"})["status"] == "warn"


def test_migration_backup_gate_apply_rollback_and_quality(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "sample.json").write_text('{"ok": true, "live_trading_enabled": false}', encoding="utf-8")
    backup = create_offline_backup(data, tmp_path / "backup.zip")
    plan = migration_plan("0.1.0", "0.2.0")
    compatibility = upgrade_compatibility("0.1.0", "0.2.0", backup=Path(backup["zip"]))
    gate = pre_upgrade_backup_gate(Path(backup["zip"]))
    dry = migration_dry_run("demo", root=data)
    blocked = migration_apply("demo", "", root=data, backup=Path(backup["zip"]), require_backup=True)
    applied = migration_apply("demo", "APPLY_LOCAL_MIGRATION", root=data, backup=Path(backup["zip"]), require_backup=True)
    rollback = rollback_plan("0.1.0", backup=Path(backup["zip"]))
    validation = post_upgrade_validation(data)
    quality = release_quality_gate([gate, dry, validation])

    assert migration_registry()["status"] == "ready"
    assert plan["status"] == "ok"
    assert compatibility["status"] in {"ok", "warning"}
    assert verify_backup(Path(backup["zip"]))["status"] == "ok"
    assert gate["status"] == "ok"
    assert dry["source_modified"] is False
    assert blocked["status"] == "blocked"
    assert applied["status"] == "applied"
    assert rollback["status"] == "ok"
    assert quality["status"] in {"ok", "warn"}


def test_release_candidate_evidence_bundle_and_legacy_surface(tmp_path: Path) -> None:
    candidate = release_candidate("0.2.0", root=tmp_path)
    manifest = create_release_manifest(tmp_path, "0.2.0")
    bundle = export_release_evidence_bundle([Path(manifest["path"])], tmp_path / "evidence")
    verified = verify_release_evidence_bundle(Path(bundle["manifest"]))
    version = version_payload("1.2.3")

    assert candidate["status"] in {"ready", "blocked"}
    assert bundle["redaction_proof"] is True
    assert verified["status"] == "ok"
    assert version["payload"]["version"] == "1.2.3"
    assert version["payload"]["schema_version"] == "1"
