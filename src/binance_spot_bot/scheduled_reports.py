from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .local_jobs import LocalJobDefinition, LocalJobSchedule
from .redaction import redact_payload


def default_scheduled_report_jobs() -> list[LocalJobDefinition]:
    return [
        LocalJobDefinition("daily-paper-deployment", "Daily paper deployment", "Daily paper deployment report.", "paper-deployment-cycle", ["--json"], LocalJobSchedule("daily", {"time": "18:00"}), category="report"),
        LocalJobDefinition("daily-data-quality", "Daily data quality", "Daily data quality report.", "data-quality", ["--json"], LocalJobSchedule("daily", {"time": "18:05"}), category="report"),
        LocalJobDefinition("daily-local-ops", "Daily local ops snapshot", "Daily local ops snapshot.", "local-ops-snapshot", ["--json"], LocalJobSchedule("daily", {"time": "18:10"}), category="report"),
        LocalJobDefinition("weekly-governance", "Weekly governance", "Weekly governance report.", "weekly-governance-report", ["--json"], LocalJobSchedule("weekly", {"weekday": "monday", "time": "09:00"}), category="governance"),
        LocalJobDefinition("weekly-support-verify", "Weekly support verify", "Weekly support bundle verification.", "support-bundles-verify", ["--json"], LocalJobSchedule("weekly", {"weekday": "friday", "time": "16:00"}), category="diagnostics"),
        LocalJobDefinition("weekly-data-growth", "Weekly data growth", "Weekly data growth budget.", "data-growth-budget", ["--json"], LocalJobSchedule("weekly", {"weekday": "friday", "time": "16:10"}), category="cleanup"),
    ]


def scheduled_report_plan() -> dict[str, Any]:
    jobs = default_scheduled_report_jobs()
    return {"status": "ready", "jobs": [job.to_dict() for job in jobs], "live_trading_enabled": False}


def write_scheduled_report(root: Path, name: str, payload: dict[str, Any]) -> Path:
    out = root / "local-ops" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.json"
    path.write_text(json.dumps(redact_payload({**payload, "live_trading_enabled": False}), indent=2, default=str), encoding="utf-8")
    return path
