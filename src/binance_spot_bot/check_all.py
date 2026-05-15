from __future__ import annotations

import json
import importlib.util
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class CheckResult:
    name: str
    status: str
    returncode: int
    stdout_tail: str = ""
    stderr_tail: str = ""


def run_command(name: str, command: list[str], root: Path) -> CheckResult:
    env = dict(os.environ)
    temp_root = root / ".tmp" / "check-all-temp"
    temp_root.mkdir(parents=True, exist_ok=True)
    env["PYTHONPATH"] = "src"
    env["LIVE_TRADING_ENABLED"] = "false"
    env["KILL_SWITCH"] = "true"
    env["TMP"] = str(temp_root)
    env["TEMP"] = str(temp_root)
    env["TMPDIR"] = str(temp_root)
    completed = subprocess.run(command, cwd=root, env=env, text=True, capture_output=True, timeout=120)
    return CheckResult(
        name=name,
        status="ok" if completed.returncode == 0 else "failed",
        returncode=completed.returncode,
        stdout_tail="\n".join(completed.stdout.splitlines()[-20:]),
        stderr_tail="\n".join(completed.stderr.splitlines()[-20:]),
    )


def run_checks(root: Path, skip_tests: bool = False) -> list[CheckResult]:
    checks: list[tuple[str, list[str]]] = []
    if not skip_tests:
        checks.append(("unit_tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests"]))
    checks.extend(
        [
            ("config_validation", [sys.executable, "-m", "binance_spot_bot.cli", "validate-config"]),
            ("preflight", [sys.executable, "-m", "binance_spot_bot.cli", "preflight"]),
            ("security_scan", [sys.executable, "-m", "binance_spot_bot.cli", "security-scan"]),
            ("dashboard_import", [sys.executable, "-c", "import binance_spot_bot.ui.streamlit_app"]),
            ("diagnostics_cli", [sys.executable, "-m", "binance_spot_bot.cli", "diagnostics", "--json"]),
            ("support_bundle_cli", [sys.executable, "-m", "binance_spot_bot.cli", "support-bundle", "--json"]),
            ("operator_quality_gate_cli", [sys.executable, "-m", "binance_spot_bot.cli", "operator-quality-gate", "--json"]),
            ("local_ops_snapshot_cli", [sys.executable, "-m", "binance_spot_bot.cli", "local-ops-snapshot", "--json"]),
            ("pilot_orchestrator_import", [sys.executable, "-c", "import binance_spot_bot.pilot_orchestrator"]),
            ("pilot_runner_import", [sys.executable, "-c", "import binance_spot_bot.pilot_runner"]),
            (
                "pilot_store_smoke",
                [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; import uuid; from binance_spot_bot.pilot_orchestrator import PilotRunStore; s=PilotRunStore(Path('.tmp')/'check-all-temp'/('pilot-store-'+uuid.uuid4().hex)/'runs'); v='abcde'*6; r=s.create_run('binance-demo-spot','BTCUSDT','smoke','blocked',[{'reason':'secret='+v}]); assert s.load(r.run_id).blockers[0]['reason']=='[REDACTED]'",
                ],
            ),
            (
                "pilot_runner_status_smoke",
                [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; import uuid; from binance_spot_bot.config import BotSettings; from binance_spot_bot.pilot_runner import PilotRunnerService; from dataclasses import replace; s=replace(BotSettings.from_env(), data_dir=Path('.tmp')/'check-all-temp'/('pilot-runner-'+uuid.uuid4().hex)/'data'); p=PilotRunnerService(s).status(); assert p['runner']['state']=='not_running'",
                ],
            ),
            ("cli_smoke", [sys.executable, "-m", "binance_spot_bot.cli", "launch-dashboard", "--start-port", "8700"]),
            ("dashboard_v2_import", [sys.executable, "-c", "import binance_spot_bot.dashboard_v2"]),
            ("dashboard_v2_api_smoke", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-api-smoke", "--json"]),
            ("dashboard_v2_page_parity", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-page-parity", "--json"]),
            ("dashboard_v2_performance_budget", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-performance-budget", "--json"]),
            ("dashboard_v2_cutover_readiness", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-cutover-readiness", "--json"]),
            ("dashboard_v2_ux_backlog", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-ux-backlog", "--json"]),
            ("dashboard_v2_streamlit_deprecation", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-streamlit-deprecation-readiness", "--json"]),
            ("dashboard_v2_final_parity_lock", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-final-parity-lock", "--json"]),
            ("dashboard_v2_deprecation_gate", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-deprecation-gate", "--json"]),
            ("dashboard_v2_only_smoke", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-only-smoke", "--json"]),
            ("dashboard_v2_removal_readiness_gate", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-removal-readiness-gate", "--json"]),
            ("dashboard_v2_dependency_isolation", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-dependency-isolation", "--json"]),
            ("dashboard_v2_check_all_v2_only", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-check-all", "--profile", "v2-only", "--json"]),
            ("dashboard_v2_workspace_presets", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-workspace-presets", "--json"]),
            ("dashboard_v2_widget_registry", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-widget-registry", "--json"]),
            ("dashboard_v2_analytics_query", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-analytics-query", "--scope", "runtime_snapshot", "--json"]),
            ("dashboard_v2_extension_packs", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-extension-packs", "--json"]),
            ("dashboard_v2_template_packs", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-template-packs", "--json"]),
            ("dashboard_v2_pack_recommendations", [sys.executable, "-m", "binance_spot_bot.cli", "dashboard-v2-pack-recommendations", "--workflow", "paper-session", "--json"]),
            ("no_live_ui", [sys.executable, "-c", "from binance_spot_bot.ui.state import SELECTABLE_MODES; assert 'live' not in SELECTABLE_MODES"]),
            ("no_secret_artifacts", [sys.executable, "-m", "binance_spot_bot.cli", "security-scan"]),
        ]
    )
    results = [run_command(name, command, root) for name, command in checks]
    results.append(_ruff_check(root))
    return results


def _ruff_check(root: Path) -> CheckResult:
    if importlib.util.find_spec("ruff") is None:
        return CheckResult("ruff", "ok", 0, "ruff not installed; optional check skipped")
    return run_command("ruff", [sys.executable, "-m", "ruff", "check", "src", "tests"], root)


def payload_for(results: list[CheckResult]) -> dict[str, object]:
    return {
        "status": "ok" if all(item.status == "ok" for item in results) else "failed",
        "checks": [asdict(item) for item in results],
    }


def print_payload(payload: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2))
        return
    for item in payload["checks"]:
        assert isinstance(item, dict)
        print(f"[{item['status']}] {item['name']}")
        if item["status"] != "ok":
            if item.get("stdout_tail"):
                print(item["stdout_tail"])
            if item.get("stderr_tail"):
                print(item["stderr_tail"])
    print(payload["status"])
