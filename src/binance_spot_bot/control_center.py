from __future__ import annotations

import os
import subprocess
import sys
import time
import webbrowser
from dataclasses import asdict, dataclass
from pathlib import Path

from .launcher import dashboard_command, find_free_port


@dataclass(frozen=True)
class ControlCenterLaunch:
    status: str
    url: str
    port: int
    pid: int | None
    log_path: str
    error_log_path: str
    live_trading_enabled: bool
    kill_switch: bool
    command: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def safe_environment(project_root: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = "src"
    env["LIVE_TRADING_ENABLED"] = "false"
    env["KILL_SWITCH"] = "true"
    env.setdefault("DATA_DIR", str(project_root / "data"))
    env.setdefault("AUDIT_LOG_PATH", str(project_root / "data" / "audit" / "events.jsonl"))
    return env


def build_launch_plan(project_root: Path, start_port: int = 8503) -> ControlCenterLaunch:
    port = find_free_port(start_port)
    logs_dir = project_root / "data" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    command = dashboard_command(project_root, port)
    return ControlCenterLaunch(
        status="planned",
        url=f"http://127.0.0.1:{port}",
        port=port,
        pid=None,
        log_path=str(logs_dir / "control-center.log"),
        error_log_path=str(logs_dir / "control-center.err.log"),
        live_trading_enabled=False,
        kill_switch=True,
        command=command,
    )


def start_control_center(project_root: Path, start_port: int = 8503, open_browser: bool = True, dry_run: bool = False) -> ControlCenterLaunch:
    plan = build_launch_plan(project_root, start_port)
    if dry_run:
        return plan
    env = safe_environment(project_root)
    preflight = subprocess.run(
        [sys.executable, "-m", "binance_spot_bot.cli", "preflight"],
        cwd=project_root,
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    if preflight.returncode != 0:
        Path(plan.error_log_path).write_text(preflight.stderr + preflight.stdout, encoding="utf-8")
        return ControlCenterLaunch(
            status="preflight_failed",
            url=plan.url,
            port=plan.port,
            pid=None,
            log_path=plan.log_path,
            error_log_path=plan.error_log_path,
            live_trading_enabled=False,
            kill_switch=True,
            command=plan.command,
        )
    with open(plan.log_path, "w", encoding="utf-8") as stdout, open(plan.error_log_path, "w", encoding="utf-8") as stderr:
        process = subprocess.Popen(plan.command, cwd=project_root, env=env, stdout=stdout, stderr=stderr)
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            import socket

            with socket.create_connection(("127.0.0.1", plan.port), timeout=0.5):
                if open_browser:
                    webbrowser.open(plan.url)
                return ControlCenterLaunch(
                    status="running",
                    url=plan.url,
                    port=plan.port,
                    pid=process.pid,
                    log_path=plan.log_path,
                    error_log_path=plan.error_log_path,
                    live_trading_enabled=False,
                    kill_switch=True,
                    command=plan.command,
                )
        except OSError:
            time.sleep(0.5)
    return ControlCenterLaunch(
        status="unreachable",
        url=plan.url,
        port=plan.port,
        pid=process.pid,
        log_path=plan.log_path,
        error_log_path=plan.error_log_path,
        live_trading_enabled=False,
        kill_switch=True,
        command=plan.command,
    )
