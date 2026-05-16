from __future__ import annotations

import os
import json
import subprocess
import sys
import time
import webbrowser
from dataclasses import asdict, dataclass
from pathlib import Path

from .dashboard_evidence import write_launch_evidence
from .config import BotSettings
from .diagnostics import collect_diagnostics
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
    evidence_path: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def safe_environment(project_root: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(project_root / "src")
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
        log_path=str(logs_dir / "dashboard-v2.log"),
        error_log_path=str(logs_dir / "dashboard-v2.err.log"),
        live_trading_enabled=False,
        kill_switch=True,
        command=command,
    )


def start_control_center(project_root: Path, start_port: int = 8503, open_browser: bool = True, dry_run: bool = False) -> ControlCenterLaunch:
    plan = build_launch_plan(project_root, start_port)
    if dry_run:
        return _with_evidence(project_root, plan, "not_run")
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
        return _with_evidence(
            project_root,
            ControlCenterLaunch(
            status="preflight_failed",
            url=plan.url,
            port=plan.port,
            pid=None,
            log_path=plan.log_path,
            error_log_path=plan.error_log_path,
            live_trading_enabled=False,
            kill_switch=True,
            command=plan.command,
            ),
            "failed",
        )
    with open(plan.log_path, "w", encoding="utf-8") as stdout, open(plan.error_log_path, "w", encoding="utf-8") as stderr:
        process = subprocess.Popen(plan.command, cwd=project_root, env=env, stdout=stdout, stderr=stderr)
    pid_file = project_root / "data" / "logs" / "dashboard.pid"
    pid_file.write_text(str(process.pid), encoding="utf-8")
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            import socket

            with socket.create_connection(("127.0.0.1", plan.port), timeout=0.5):
                if open_browser:
                    webbrowser.open(plan.url)
                return _with_evidence(
                    project_root,
                    ControlCenterLaunch(
                    status="running",
                    url=plan.url,
                    port=plan.port,
                    pid=process.pid,
                    log_path=plan.log_path,
                    error_log_path=plan.error_log_path,
                    live_trading_enabled=False,
                    kill_switch=True,
                    command=plan.command,
                    ),
                    "ok",
                )
        except OSError:
            time.sleep(0.5)
    return _with_evidence(
        project_root,
        ControlCenterLaunch(
            status="unreachable",
            url=plan.url,
            port=plan.port,
            pid=process.pid,
            log_path=plan.log_path,
            error_log_path=plan.error_log_path,
            live_trading_enabled=False,
            kill_switch=True,
            command=plan.command,
        ),
        "ok",
    )


def _with_evidence(project_root: Path, launch: ControlCenterLaunch, preflight_status: str) -> ControlCenterLaunch:
    launch_payload = launch.to_dict()
    try:
        diagnostics = collect_diagnostics(BotSettings.from_env()).to_dict()
        launch_payload["diagnostics_status"] = diagnostics.get("status", "unknown")
        launch_payload["diagnostics_next_safe_action"] = diagnostics.get("next_safe_action", "")
    except Exception as exc:
        launch_payload["diagnostics_status"] = "unavailable"
        launch_payload["diagnostics_error"] = str(exc)
    evidence_path = write_launch_evidence(project_root / "data", launch_payload, preflight_status=preflight_status)
    completed = ControlCenterLaunch(**{**launch.to_dict(), "evidence_path": str(evidence_path)})
    launcher_dir = project_root / "data" / "dashboard-v2" / "launcher"
    launcher_dir.mkdir(parents=True, exist_ok=True)
    (launcher_dir / "last-launch.json").write_text(json.dumps(completed.to_dict(), indent=2, default=str), encoding="utf-8")
    return completed
