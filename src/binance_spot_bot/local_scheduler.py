from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .local_job_runner import run_local_job
from .local_job_store import LocalJobStore
from .local_jobs import LocalJobDefinition


def due_jobs(jobs: list[dict[str, Any]], now_ms: int) -> dict[str, Any]:
    due = [job for job in jobs if bool(job.get("enabled", True)) and int(job.get("next_due_ms", 0)) <= now_ms]
    return {"status": "ready", "jobs": due, "live_trading_enabled": False}


def find_due_jobs(definitions: list[LocalJobDefinition], *, now_ms: int | None = None) -> list[LocalJobDefinition]:
    now_ms = now_ms or int(time.time() * 1000)
    due: list[LocalJobDefinition] = []
    for job in definitions:
        if not job.enabled:
            continue
        cfg = job.schedule.config
        next_due = int(cfg.get("next_due_ms", 0))
        if job.schedule.schedule_type in {"manual", "on_failure", "on_shutdown"}:
            continue
        if next_due <= now_ms:
            due.append(job)
    return due


def scheduler_tick(root: Path, *, dry_run: bool = True, now_ms: int | None = None, concurrency_limit: int = 1) -> dict[str, Any]:
    store = LocalJobStore(root / "local-jobs")
    jobs = store.load_jobs()
    due = find_due_jobs(jobs, now_ms=now_ms)
    if _lock_exists(root):
        return {"status": "locked", "due": [job.job_id for job in due], "live_trading_enabled": False}
    results: list[dict[str, Any]] = []
    if dry_run:
        return {"status": "dry_run", "due": [job.job_id for job in due], "results": [], "live_trading_enabled": False}
    _write_lock(root)
    try:
        for job in due[: max(1, concurrency_limit)]:
            results.append(run_local_job(job, root=root, execute=True).copy())
    finally:
        _clear_lock(root)
    return {"status": "ok", "due": [job.job_id for job in due], "results": results, "live_trading_enabled": False}


def _lock_path(root: Path) -> Path:
    return root / "local-ops" / "scheduler.lock.json"


def _lock_exists(root: Path) -> bool:
    return _lock_path(root).exists()


def _write_lock(root: Path) -> None:
    path = _lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"created_at_ms": int(time.time() * 1000), "live_trading_enabled": False}), encoding="utf-8")


def _clear_lock(root: Path) -> None:
    _lock_path(root).unlink(missing_ok=True)
