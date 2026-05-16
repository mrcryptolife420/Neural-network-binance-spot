from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .experiment_queue import StrategyExperimentJob, StrategyExperimentQueue, queue_manifest, queue_to_dict, validate_queue


class StrategyExperimentQueueStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.queued = self.root / "queued"
        self.completed = self.root / "completed"
        self.reports = self.root / "reports"
        for path in (self.queued, self.completed, self.reports):
            path.mkdir(parents=True, exist_ok=True)

    def _path(self, queue_id: str, folder: Path | None = None) -> Path:
        if any(part in queue_id for part in ("..", "/", "\\")):
            raise ValueError("invalid queue id")
        return (folder or self.queued) / f"{queue_id}.json"

    def save(self, queue_payload: dict[str, Any]) -> dict[str, Any]:
        safe = redact_payload(queue_payload)
        path = self._path(str(safe["queue_id"]))
        path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
        return {"status": "ok", "path": str(path), "queue": safe, "live_trading_enabled": False}

    def load(self, queue_id: str) -> dict[str, Any]:
        for folder in (self.queued, self.completed):
            path = self._path(queue_id, folder)
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
        raise FileNotFoundError(queue_id)

    def list(self) -> dict[str, Any]:
        queues = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(self.queued.glob("*.json"))]
        return {"status": "ok", "queues": queues, "live_trading_enabled": False}

    def update_job_status(self, queue_id: str, job_id: str, status: str) -> dict[str, Any]:
        payload = self.load(queue_id)
        for job in payload.get("jobs", []):
            if job.get("job_id") == job_id:
                job["status"] = status
        return self.save(payload)

    def export_manifest(self, queue_id: str) -> dict[str, Any]:
        payload = self.load(queue_id)
        jobs = tuple(StrategyExperimentJob(**job) for job in payload.get("jobs", []))
        queue = StrategyExperimentQueue(payload["queue_id"], payload.get("name", "Strategy Lab Queue"), jobs)
        manifest = queue_manifest(queue)
        path = self.reports / f"{queue_id}.manifest.json"
        path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return {"status": "ok", "manifest": manifest, "path": str(path), "live_trading_enabled": False}

    def validate(self, queue_id: str) -> dict[str, Any]:
        payload = self.load(queue_id)
        jobs = tuple(StrategyExperimentJob(**job) for job in payload.get("jobs", []))
        return validate_queue(StrategyExperimentQueue(payload["queue_id"], payload.get("name", "Strategy Lab Queue"), jobs))


def default_strategy_queue_store(root: Path | str = ".") -> StrategyExperimentQueueStore:
    return StrategyExperimentQueueStore(Path(root) / "data" / "strategy-lab" / "queues")
