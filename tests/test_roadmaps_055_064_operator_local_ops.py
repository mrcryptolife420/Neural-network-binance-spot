from __future__ import annotations

import io
import json
import os
import zipfile
from contextlib import redirect_stdout
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.config import BotSettings
from binance_spot_bot.operator_ops import (
    artifact_catalog,
    data_growth_budget,
    environment_doctor,
    evidence_chain,
    operator_command_manifest,
    operator_health_score,
    operator_report_diff,
    rehearsal_profiles,
    support_bundle_restore_preview,
)


def settings(tmp_path: Path) -> BotSettings:
    return replace(
        BotSettings.from_env(),
        data_dir=tmp_path / "data",
        audit_log_path=tmp_path / "data" / "audit" / "events.jsonl",
    )


def test_055_operator_health_score_action_priority_engine(tmp_path: Path) -> None:
    payload = operator_health_score(settings(tmp_path))

    assert payload["live_trading_enabled"] is False
    assert 0 <= payload["score"] <= 100
    assert payload["grade"] in {"A", "B", "C", "D"}
    assert payload["priorities"]
    assert payload["next_best_action"]


def test_056_artifact_catalog_filters_staleness_and_groups(tmp_path: Path) -> None:
    s = settings(tmp_path)
    artifact = s.data_dir / "checks" / "check-all.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text('{"status":"ok"}', encoding="utf-8")
    (s.data_dir / "reports").mkdir(parents=True, exist_ok=True)
    (s.data_dir / "reports" / "operator.txt").write_text("report", encoding="utf-8")

    payload = artifact_catalog(s, category="checks", suffix=".json", stale_days=0)

    assert payload["count"] == 1
    assert payload["artifacts"][0]["category"] == "checks"
    assert payload["summaries"]["by_category"]["checks"]["count"] == 1
    assert "stale_count" in payload["summaries"]


def test_057_rehearsal_profiles_fast_standard_deep() -> None:
    payload = rehearsal_profiles()
    names = {row["name"] for row in payload["profiles"]}

    assert payload["live_trading_enabled"] is False
    assert {"fast", "standard", "deep"} <= names
    assert all(row["steps"] for row in payload["profiles"])


def test_058_operator_report_diff_empty_and_single_report(tmp_path: Path) -> None:
    s = settings(tmp_path)
    assert operator_report_diff(s)["status"] == "empty"

    report_dir = s.data_dir / "reports" / "operator"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "operator-report.md").write_text("# Report\n", encoding="utf-8")

    payload = operator_report_diff(s)
    assert payload["status"] == "single"
    assert payload["live_trading_enabled"] is False


def test_059_support_bundle_restore_preview_is_non_destructive(tmp_path: Path) -> None:
    bundle = tmp_path / "support-bundle.zip"
    manifest = {
        "files": [
            {"path": "diagnostics.json", "size_bytes": 2, "sha256": "00", "redacted": True},
            {"path": "settings-redacted.json", "size_bytes": 2, "sha256": "00", "redacted": True},
        ],
        "live_trading_enabled": False,
    }
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.writestr("manifest.json", json.dumps(manifest))

    payload = support_bundle_restore_preview(bundle)

    assert payload["status"] == "ok"
    assert payload["mode"] == "preview-only"
    assert payload["redacted"] is True


def test_060_evidence_integrity_chain_writes_redacted_hash_manifest(tmp_path: Path) -> None:
    s = settings(tmp_path)
    artifact = s.data_dir / "checks" / "check-all.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text('{"status":"ok"}', encoding="utf-8")

    payload = evidence_chain(s)
    chain_path = Path(payload["path"])
    chain = json.loads(chain_path.read_text(encoding="utf-8"))

    assert payload["live_trading_enabled"] is False
    assert payload["count"] >= 1
    assert chain["chain"][0]["sha256"].count("-") >= 1


def test_061_dashboard_command_palette_and_local_ops_panels_are_registered() -> None:
    source = Path("src/binance_spot_bot/ui/streamlit_app.py").read_text(encoding="utf-8")

    assert "Local Ops Command Palette" in source
    assert "Operator health score" in source
    assert "Evidence integrity chain hashes" in source
    assert "Data growth budget forecast" in source


def test_062_environment_doctor_checks_python_deps_and_paths(tmp_path: Path) -> None:
    payload = environment_doctor(settings(tmp_path))
    checks = {row["check"]: row for row in payload["checks"]}

    assert payload["live_trading_enabled"] is False
    assert checks["python"]["status"] == "ok"
    assert checks["data_dir"]["status"] == "ok"
    assert "package_pytest" in checks


def test_063_data_growth_budget_forecast(tmp_path: Path) -> None:
    s = settings(tmp_path)
    artifact = s.data_dir / "checks" / "large.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("x" * 128, encoding="utf-8")

    payload = data_growth_budget(s, budget_bytes=64)

    assert payload["status"] == "warn"
    assert payload["total_size_bytes"] >= 128
    assert payload["budget_used_pct"] > 100
    assert payload["largest_files"]


def test_064_local_ops_cli_new_commands_return_json_without_live(tmp_path: Path) -> None:
    env = {"DATA_DIR": str(tmp_path / "data"), "AUDIT_LOG_PATH": str(tmp_path / "data" / "audit" / "events.jsonl")}
    commands = [
        ["operator-health-score", "--json"],
        ["rehearsal-profiles", "--json"],
        ["operator-report-diff", "--json"],
        ["evidence-chain", "--json"],
        ["environment-doctor", "--json"],
        ["data-growth-budget", "--budget-bytes", "100000", "--json"],
        ["operator-command-manifest", "--json"],
    ]

    for command in commands:
        buf = io.StringIO()
        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", *command]), redirect_stdout(buf):
            cli_main()
        payload = json.loads(buf.getvalue())
        assert payload["live_trading_enabled"] is False

    manifest = operator_command_manifest()
    names = {row["command"] for row in manifest["commands"]}
    assert {"operator-health-score", "environment-doctor", "data-growth-budget"} <= names
