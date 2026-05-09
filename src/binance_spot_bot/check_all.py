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
    env["PYTHONPATH"] = "src"
    env["LIVE_TRADING_ENABLED"] = "false"
    env["KILL_SWITCH"] = "true"
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
            ("cli_smoke", [sys.executable, "-m", "binance_spot_bot.cli", "launch-dashboard", "--start-port", "8700"]),
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
