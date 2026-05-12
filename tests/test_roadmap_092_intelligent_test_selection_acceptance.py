from pathlib import Path

from binance_spot_bot.changed_files import detect_changed_files
from binance_spot_bot.check_all_v2 import SAFE_ENV, run_selected_checks
from binance_spot_bot.flaky_tests import flaky_tests, write_flaky_test_report
from binance_spot_bot.intelligent_test_selector import select_intelligent_tests, selected_tests
from binance_spot_bot.regression_risk import score_regression_risk
from binance_spot_bot.regression_risk_report import build_regression_risk_report, write_regression_risk_report
from binance_spot_bot.test_evidence_bundle import export_test_evidence_bundle, verify_test_evidence_bundle
from binance_spot_bot.test_inventory import build_test_inventory, verify_test_inventory_manifest, write_test_inventory_manifest
from binance_spot_bot.test_profiles import test_profiles as build_test_profiles, validate_profile_for_risk
from binance_spot_bot.test_runtime_history import append_test_runtime_history, summarize_test_runtime_history


def _fixture_tests(root: Path) -> None:
    tests = root / "tests"
    tests.mkdir()
    (tests / "test_runtime.py").write_text(
        "from binance_spot_bot.runtime import BotRuntime\n\n"
        "class TestRuntime:\n    pass\n\n"
        "def test_runtime_smoke():\n    assert True\n",
        encoding="utf-8",
    )


def test_test_inventory_manifest_and_runtime_history(tmp_path: Path):
    _fixture_tests(tmp_path)
    inventory = build_test_inventory(tmp_path)
    assert inventory["payload"]["count"] == 1
    assert inventory["payload"]["tests"][0]["test_count"] == 2
    manifest = write_test_inventory_manifest(tmp_path)
    assert verify_test_inventory_manifest(Path(manifest["path"]).parent / "test-inventory-manifest.json")["status"] == "ok"
    append_test_runtime_history(tmp_path, {"command": "pytest", "status": "ok", "returncode": 0, "duration_ms": 12})
    summary = summarize_test_runtime_history(tmp_path)
    assert summary["count"] == 1


def test_changed_files_risk_profiles_and_selector(tmp_path: Path):
    changed = ["src/binance_spot_bot/runtime.py", "src/binance_spot_bot/redaction.py"]
    detected = detect_changed_files(tmp_path, changed)
    assert detected["payload"]["files"][0]["owner"] == "runtime"
    risk = score_regression_risk(changed)
    assert risk["payload"]["level"] == "critical"
    assert validate_profile_for_risk("fast", "critical")["status"] == "blocked"
    profiles = build_test_profiles()
    assert any(item["name"] == "deep" for item in profiles["payload"]["profiles"])
    selection = select_intelligent_tests(changed, policy="strict")
    assert selection["selected_profile"] == "deep"
    legacy = selected_tests(["src/binance_spot_bot/security.py"])
    assert "tests/test_risk_execution_security.py" in legacy["payload"]["tests"]


def test_check_all_v2_evidence_flaky_and_reports(tmp_path: Path):
    _fixture_tests(tmp_path)
    result = run_selected_checks(tmp_path, ["src/binance_spot_bot/runtime.py"], execute=False)
    assert result["status"] == "ok"
    assert result["safe_env"] == SAFE_ENV
    assert summarize_test_runtime_history(tmp_path)["count"] >= 1
    flaky = flaky_tests([{"command": "pytest", "status": "ok"}, {"command": "pytest", "status": "failed"}])
    assert flaky["candidates"]
    flaky_report = write_flaky_test_report(tmp_path, [{"command": "pytest", "status": "ok"}, {"command": "pytest", "status": "failed"}])
    assert Path(flaky_report["paths"]["json"]).exists()
    report = build_regression_risk_report(["src/binance_spot_bot/runtime.py"])
    report_paths = write_regression_risk_report(tmp_path, report)
    assert Path(report_paths["json"]).exists()
    bundle = export_test_evidence_bundle([Path(report_paths["json"])], tmp_path / "evidence")
    assert verify_test_evidence_bundle(bundle["manifest"])["status"] == "ok"
