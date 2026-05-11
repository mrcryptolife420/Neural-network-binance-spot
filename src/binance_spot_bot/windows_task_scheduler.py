from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .local_job_allowlist import is_safe_command
from .redaction import redact_payload


def windows_task_plan(cmd: str, name: str = "SpotBotLocalOps", *, repo_root: Path | None = None) -> dict[str, Any]:
    allowed = is_safe_command(cmd)
    root = repo_root or Path.cwd()
    safe_env = {"LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"}
    cli_cmd = cmd if cmd.strip().startswith("python -m binance_spot_bot.cli") else f"python -m binance_spot_bot.cli {cmd}"
    command = f"cd /d \"{root}\" && {cli_cmd}"
    return redact_payload(
        {
            "status": "ready" if allowed else "blocked",
            "name": name,
            "cmd": cmd,
            "command_line": command,
            "allowed": allowed,
            "safe_env": safe_env,
            "live_trading_enabled": False,
        }
    )


def write_windows_scheduler_scripts(root: Path, repo_root: Path, *, confirm: str = "") -> dict[str, str]:
    out = root / "scripts"
    out.mkdir(parents=True, exist_ok=True)
    scripts = {
        "run-local-ops-tick.ps1": "python -m binance_spot_bot.cli local-scheduler-tick --json",
        "run-daily-paper-report.ps1": "python -m binance_spot_bot.cli scheduled-report-plan --default --json",
        "run-weekly-governance-report.ps1": "python -m binance_spot_bot.cli weekly-governance-report --json",
    }
    paths: dict[str, str] = {}
    for name, cmd in scripts.items():
        plan = windows_task_plan(cmd, name=name.removesuffix(".ps1"), repo_root=repo_root)
        path = out / name
        path.write_text(_script(repo_root, cmd), encoding="utf-8")
        paths[name] = str(path)
        paths[f"{name}.plan"] = json.dumps(plan, default=str)
    install = out / "install-local-ops-scheduler.ps1"
    uninstall = out / "uninstall-local-ops-scheduler.ps1"
    install.write_text(_confirm_script("INSTALL_LOCAL_OPS", confirm, "Install local paper ops scheduler tasks."), encoding="utf-8")
    uninstall.write_text(_confirm_script("UNINSTALL_LOCAL_OPS", confirm, "Uninstall local paper ops scheduler tasks."), encoding="utf-8")
    paths["install-local-ops-scheduler.ps1"] = str(install)
    paths["uninstall-local-ops-scheduler.ps1"] = str(uninstall)
    return paths


def _script(repo_root: Path, cmd: str) -> str:
    safe_root = str(repo_root).replace("'", "''")
    return "\n".join(
        [
            "$ErrorActionPreference = 'Stop'",
            "$env:LIVE_TRADING_ENABLED = 'false'",
            "$env:KILL_SWITCH = 'true'",
            f"Set-Location -LiteralPath '{safe_root}'",
            cmd,
            "",
        ]
    )


def _confirm_script(required: str, confirm: str, message: str) -> str:
    status = "ready" if confirm == required else "confirmation_required"
    return f"# {message}\n# Status: {status}\n# Required confirmation: {required}\n"
