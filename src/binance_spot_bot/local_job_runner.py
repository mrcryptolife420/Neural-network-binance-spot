from __future__ import annotations

import os
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .local_job_allowlist import parse_local_command, validate_local_job_command
from .local_job_store import LocalJobStore
from .local_jobs import LocalJobDefinition, LocalJobResult, LocalJobRun
from .redaction import redact_payload


def run_local_job(
    job_or_command: LocalJobDefinition | str,
    *,
    root: Path | None = None,
    execute: bool = False,
    cwd: Path | None = None,
) -> dict[str, Any]:
    job = job_or_command if isinstance(job_or_command, LocalJobDefinition) else _job_from_command(job_or_command)
    validation = validate_local_job_command(job.command, job.args)
    if not job.enabled:
        return {"status": "disabled", "job_id": job.job_id, "reasons": ["job_disabled"], "live_trading_enabled": False}
    if not validation.allowed:
        return {"status": "blocked", "job_id": job.job_id, "validation": validation.to_dict(), "live_trading_enabled": False}
    if not execute:
        return {"status": "ready", "job_id": job.job_id, "validation": validation.to_dict(), "live_trading_enabled": False}
    return execute_local_job(job, root=root or Path("data/local-ops"), cwd=cwd or Path.cwd()).to_dict()


def execute_local_job(job: LocalJobDefinition, *, root: Path, cwd: Path) -> LocalJobResult:
    started = int(time.time() * 1000)
    run_id = f"{job.job_id}-{started}"
    validation = validate_local_job_command(job.command, job.args)
    if not validation.allowed:
        return LocalJobResult(job.job_id, run_id, "blocked", 1, stderr_tail=";".join(validation.reasons))
    cmd, args = parse_local_command(job.command, job.args)
    env = _safe_env()
    completed: subprocess.CompletedProcess[str] | None = None
    timed_out = False
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "binance_spot_bot.cli", cmd, *args],
            cwd=str(cwd),
            env=env,
            text=True,
            capture_output=True,
            timeout=job.max_runtime_seconds,
            check=False,
        )
        status = "ok" if completed.returncode == 0 else "failed"
        returncode = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        status = "timeout"
        returncode = 124
        stdout = exc.stdout or ""
        stderr = exc.stderr or "timeout"
    result = LocalJobResult(
        job_id=job.job_id,
        run_id=run_id,
        status=status,
        returncode=returncode,
        stdout_tail=str(redact_payload(stdout))[-2000:],
        stderr_tail=str(redact_payload(stderr))[-2000:],
        failure_action=job.failure_policy.action if status != "ok" else "none",
    )
    run = LocalJobRun(run_id, job.job_id, status, started, int(time.time() * 1000), returncode)
    store = LocalJobStore(root / "local-jobs")
    store.save_run(run, result, str(stdout), str(stderr))
    if status != "ok" and job.failure_policy.create_support_bundle:
        _create_failure_marker(root, job, result, timed_out)
    return result


def _safe_env() -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if "BINANCE_API_SECRET" not in key and "BINANCE_API_KEY" not in key}
    env["LIVE_TRADING_ENABLED"] = "false"
    env["KILL_SWITCH"] = "true"
    return env


def _job_from_command(command: str) -> LocalJobDefinition:
    cmd, args = parse_local_command(command)
    return LocalJobDefinition(
        job_id=f"manual-{cmd or 'unknown'}",
        name=f"Manual {cmd or 'unknown'}",
        description="Manual local ops job",
        command=cmd,
        args=args,
        max_runtime_seconds=60,
    )


def _create_failure_marker(root: Path, job: LocalJobDefinition, result: LocalJobResult, timed_out: bool) -> None:
    out = root / "local-ops" / "failures"
    out.mkdir(parents=True, exist_ok=True)
    marker = out / f"{result.run_id}.json"
    marker.write_text(
        json.dumps(redact_payload({"job": job.to_dict(), "result": result.to_dict(), "timed_out": timed_out, "live_trading_enabled": False}), indent=2, default=str),
        encoding="utf-8",
    )
