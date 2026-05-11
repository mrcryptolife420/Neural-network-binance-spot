from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .local_jobs import LocalJobDefinition, LocalJobResult, LocalJobRun
from .redaction import redact_payload


class LocalJobStore:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.jobs_path = self.root / "jobs.json"
        self.runs_root = self.root / "runs"

    def save_jobs(self, jobs: list[LocalJobDefinition]) -> Path:
        self.jobs_path.write_text(json.dumps([job.to_dict() for job in jobs], indent=2, default=str), encoding="utf-8")
        return self.jobs_path

    def load_jobs(self) -> list[LocalJobDefinition]:
        if not self.jobs_path.exists():
            return []
        payload = json.loads(self.jobs_path.read_text(encoding="utf-8"))
        return [LocalJobDefinition.from_dict(row) for row in payload]

    def get_job(self, job_id: str) -> LocalJobDefinition:
        for job in self.load_jobs():
            if job.job_id == job_id:
                return job
        raise KeyError(job_id)

    def save_run(self, run: LocalJobRun, result: LocalJobResult | None = None, stdout: str = "", stderr: str = "") -> Path:
        run_dir = self.runs_root / run.job_id / run.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        stdout_path = run_dir / "stdout.txt"
        stderr_path = run_dir / "stderr.txt"
        result_path = run_dir / "result.json"
        stdout_path.write_text(str(redact_payload(stdout)), encoding="utf-8")
        stderr_path.write_text(str(redact_payload(stderr)), encoding="utf-8")
        payload = run.to_dict()
        if result is not None:
            payload["result"] = result.to_dict()
        result_path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
        self._append_history(run.job_id, payload)
        return result_path

    def history(self, job_id: str | None = None) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        if not self.runs_root.exists():
            return rows
        job_dirs = [self.runs_root / job_id] if job_id else [path for path in self.runs_root.iterdir() if path.is_dir()]
        for job_dir in job_dirs:
            if not job_dir.exists():
                continue
            for result_path in job_dir.glob("*/result.json"):
                rows.append(json.loads(result_path.read_text(encoding="utf-8")))
        return sorted(rows, key=lambda row: str(row.get("started_at_ms", "")))

    def retention_preview(self, keep_last: int = 20) -> dict[str, Any]:
        deletable: list[str] = []
        for job_dir in self.runs_root.glob("*"):
            runs = sorted([path for path in job_dir.iterdir() if path.is_dir()], key=lambda path: path.name)
            deletable.extend(str(path) for path in runs[:-keep_last])
        return {"status": "preview", "deletable": deletable, "live_trading_enabled": False}

    def _append_history(self, job_id: str, payload: dict[str, Any]) -> None:
        path = self.root / "job-history.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(redact_payload({"job_id": job_id, **payload}), default=str) + "\n")


def save_local_job_run(root: Path, payload: dict[str, Any]) -> Path:
    store = LocalJobStore(root / "local-jobs")
    run = LocalJobRun(
        run_id=str(payload.get("run_id", "manual")),
        job_id=str(payload.get("job_id", "manual")),
        status=str(payload.get("status", "recorded")),
        started_at_ms=int(payload.get("started_at_ms", 0)),
        finished_at_ms=int(payload.get("finished_at_ms", 0)),
        returncode=int(payload.get("returncode", 0)),
    )
    result = LocalJobResult(run.job_id, run.run_id, run.status, int(payload.get("returncode", 0)))
    return store.save_run(run, result, str(payload.get("stdout", "")), str(payload.get("stderr", "")))
