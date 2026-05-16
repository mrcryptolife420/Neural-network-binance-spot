from __future__ import annotations

import json
import subprocess
import sys

from binance_spot_bot.packaging import NO_LIVE_AUTO_START_STATEMENT, SAFE_ENV_DEFAULTS, SECRET_FREE_PACKAGE_STATEMENT
from binance_spot_bot.packaging.package_profiles import PackageProfile, build_package_profile_report, validate_package_profile
from binance_spot_bot.packaging.packaging_pipeline import run_packaging_pipeline


def test_package_profiles_are_safe_and_serializable():
    report = build_package_profile_report()
    assert report["status"] == "ok"
    assert len(report["profiles"]) == 5
    assert report["no_live_auto_start_statement"] == NO_LIVE_AUTO_START_STATEMENT
    assert report["secret_free_package_statement"] == SECRET_FREE_PACKAGE_STATEMENT
    json.dumps(report)


def test_unsafe_package_profile_is_blocked_and_redacted():
    profile = PackageProfile(
        "unsafe",
        "Unsafe",
        "unsafe",
        extras=["unknown-extra"],
        safe_env_defaults={"LIVE_TRADING_ENABLED": "true", "KILL_SWITCH": "false"},
        forbidden_runtime_actions=[],
    )
    result = validate_package_profile(profile)
    assert result.status == "blocked"
    assert any("unknown extras" in blocker for blocker in result.blockers)
    assert any("LIVE_TRADING_ENABLED" in blocker for blocker in result.blockers)


def test_packaging_pipeline_builds_safe_artifacts(tmp_path):
    payload = run_packaging_pipeline(tmp_path)
    assert payload["status"] == "ok"
    assert payload["update"]["status"] == "blocked"
    assert "active live session" in " ".join(payload["update"]["blockers"])
    assert payload["restore"]["restore_forces_live_locked"] is True
    assert payload["rollback"]["starts_live"] is False
    assert payload["recovery_kit"]["live_order_submitted"] is False
    assert payload["safe_mode"]["runtime_auto_start"] is False
    assert payload["evidence"]["manifest"]["no_live_auto_start_proof"] is True
    assert SAFE_ENV_DEFAULTS["LIVE_TRADING_ENABLED"] == "false"


def test_packaging_cli_smokes():
    commands = [
        ["package-profiles"],
        ["package-lock"],
        ["package-build-manifest"],
        ["package-startup-health"],
        ["package-update-plan"],
        ["package-backup-create"],
        ["package-rollback-preview"],
        ["package-recovery-kit-build"],
        ["package-safe-mode-start"],
        ["package-evidence-export"],
        ["dashboard-v2-package-smoke"],
    ]
    for command in commands:
        completed = subprocess.run([sys.executable, "-m", "binance_spot_bot.cli", *command, "--json"], text=True, capture_output=True, timeout=60)
        assert completed.returncode == 0, completed.stderr
        assert "live_trading_enabled" in completed.stdout or "live_order_submitted" in completed.stdout

