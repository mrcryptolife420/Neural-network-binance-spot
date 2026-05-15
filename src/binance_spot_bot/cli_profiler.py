from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Callable

from .profiling_core import ProfileRun, profile_block, summarize_profile_run
from .redaction import redact_payload

SAFE_ENV = {"PYTHONPATH": "src", "LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"}


def profile_cli_command(root: Path | str, command: str, *, execute: bool = False, runner: Callable[[str], dict[str, Any]] | None = None) -> dict[str, Any]:
    run = ProfileRun("cli-profile", "cli")
    result: dict[str, Any]
    with profile_block(command, "cli", {"command": command}, run):
        if not execute:
            result = {"status": "planned", "returncode": 0, "stdout_tail": "", "stderr_tail": ""}
        elif runner:
            result = runner(command)
        else:
            proc = subprocess.run(command, cwd=Path(root), shell=True, env={**os.environ, **SAFE_ENV}, text=True, capture_output=True, timeout=120, check=False)
            result = {"status": "ok" if proc.returncode == 0 else "failed", "returncode": proc.returncode, "stdout_tail": proc.stdout[-1000:], "stderr_tail": proc.stderr[-1000:]}
    return {"status": result["status"], "command": command, "safe_env": SAFE_ENV, "result": redact_payload(result), "summary": summarize_profile_run(run), "run": run.to_dict(), "live_trading_enabled": False}


def cli_profile(cmd: str, elapsed_ms: float) -> dict[str, Any]:
    return {"status": "ok" if elapsed_ms <= 1000 else "warn", "payload": {"cmd": cmd, "elapsed_ms": elapsed_ms}, "live_trading_enabled": False}
