from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload


def _hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(redact_payload(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


class ExperimentResultStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.jobs = self.root / "jobs"
        self.queues = self.root / "queues"
        self.exports = self.root / "exports"
        for path in (self.jobs, self.queues, self.exports):
            path.mkdir(parents=True, exist_ok=True)

    def save_job_result(self, result: dict[str, Any]) -> dict[str, Any]:
        safe = redact_payload(result)
        safe["payload_hash"] = _hash(safe)
        path = self.jobs / f"{safe['job_id']}.json"
        path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
        return {"status": "ok", "path": str(path), "result": safe, "live_trading_enabled": False}

    def load_job_result(self, job_id: str) -> dict[str, Any]:
        if any(part in job_id for part in ("..", "/", "\\")):
            raise ValueError("invalid job id")
        return json.loads((self.jobs / f"{job_id}.json").read_text(encoding="utf-8"))

    def list_results(self) -> dict[str, Any]:
        rows = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(self.jobs.glob("*.json"))]
        return {"status": "ok", "results": rows, "live_trading_enabled": False}

    def export(self, results: list[dict[str, Any]], name: str = "strategy-lab-results") -> dict[str, Any]:
        json_path = self.exports / f"{name}.json"
        md_path = self.exports / f"{name}.md"
        csv_path = self.exports / f"{name}.csv"
        safe = redact_payload({"status": "ok", "results": results, "live_trading_enabled": False})
        json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
        md_path.write_text(f"# Strategy Lab Results\n\nRows: {len(results)}\n\nPaper-only research.\n", encoding="utf-8")
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["job_id", "symbol", "paper_pnl", "max_drawdown", "status"])
            writer.writeheader()
            for row in results:
                writer.writerow({key: row.get(key, "") for key in writer.fieldnames})
        return {"status": "ok", "json": str(json_path), "markdown": str(md_path), "csv": str(csv_path), "live_trading_enabled": False}


def default_result_store(root: Path | str = ".") -> ExperimentResultStore:
    return ExperimentResultStore(Path(root) / "data" / "strategy-lab" / "results")
