from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .config import BotSettings
from .operator_ops import operator_health_score, operator_quality_gate
from .redaction import redact_payload


@dataclass(frozen=True)
class LocalOpsJob:
    job_id: str
    cadence: str
    command: str
    output: str
    runbook: str
    blocking: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_JOBS = [
    LocalOpsJob("morning-quality-gate", "daily", "spot-bot operator-quality-gate --json", "data/reports", "Check before demo trading."),
    LocalOpsJob("evening-operator-report", "daily", "spot-bot operator-report --json", "data/reports/operator", "Review paper health and incidents."),
    LocalOpsJob("weekly-support-verify", "weekly", "spot-bot support-bundles-verify --json", "data/support", "Verify bundle restore safety."),
    LocalOpsJob("weekly-evidence-chain", "weekly", "spot-bot evidence-chain --json", "data/evidence", "Check evidence integrity chain.", blocking=True),
]


def build_ops_schedule(settings: BotSettings, jobs: list[LocalOpsJob] | None = None, *, now_ms: int | None = None) -> dict[str, Any]:
    now_ms = now_ms or int(time.time() * 1000)
    rows = []
    for job in jobs or DEFAULT_JOBS:
        rows.append(
            {
                **job.to_dict(),
                "next_due_ms": now_ms + (86_400_000 if job.cadence == "daily" else 604_800_000),
                "safe_to_run_locally": True,
                "live_trading_enabled": False,
            }
        )
    return {"status": "ready", "jobs": rows, "data_dir": str(settings.data_dir), "live_trading_enabled": False}


def write_ops_runbook(settings: BotSettings, schedule: dict[str, Any]) -> dict[str, str]:
    out = settings.data_dir / "local-ops" / "automation"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "scheduled-ops.json"
    md_path = out / "operator-runbook.md"
    json_path.write_text(json.dumps(redact_payload(schedule), indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            ["# Local Paper Ops Runbook", "", "All jobs are local paper/demo jobs. Live trading stays disabled.", ""]
            + [f"- {job['job_id']}: `{job['command']}` - {job['runbook']}" for job in schedule["jobs"]]
        ),
        encoding="utf-8",
    )
    return {"schedule": str(json_path), "runbook": str(md_path)}


def generate_scheduled_ops_report(settings: BotSettings) -> dict[str, Any]:
    schedule = build_ops_schedule(settings)
    paths = write_ops_runbook(settings, schedule)
    health = operator_health_score(settings)
    gate = operator_quality_gate(settings)
    return {
        "status": "ready" if gate.get("status") in {"ok", "warn"} else "blocked",
        "schedule": schedule,
        "health": health,
        "quality_gate": gate,
        "paths": paths,
        "live_trading_enabled": False,
    }
