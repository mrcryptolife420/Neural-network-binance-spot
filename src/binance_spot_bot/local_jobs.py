from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload

SCHEDULE_TYPES = {"manual", "daily", "weekly", "interval", "on_startup", "on_failure", "on_shutdown"}
JOB_CATEGORIES = {"report", "health", "evidence", "governance", "cleanup", "diagnostics", "drill"}


@dataclass(frozen=True)
class LocalJobSchedule:
    schedule_type: str = "manual"
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.schedule_type not in SCHEDULE_TYPES:
            raise ValueError("invalid local job schedule_type")

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class LocalJobFailurePolicy:
    action: str = "record_only"
    max_failures: int = 3
    create_support_bundle: bool = False
    create_incident_timeline: bool = False
    disable_after_failures: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class LocalJobAllowlistRule:
    command: str
    paper_only: bool = True
    read_only: bool = True
    allow_browser: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class LocalJobDefinition:
    job_id: str
    name: str
    description: str
    command: str
    args: list[str] = field(default_factory=list)
    schedule: LocalJobSchedule = field(default_factory=LocalJobSchedule)
    enabled: bool = True
    category: str = "diagnostics"
    allowlist_policy: str = "default"
    max_runtime_seconds: int = 60
    retry_policy: dict[str, Any] = field(default_factory=lambda: {"max_retries": 0, "backoff_seconds": 0})
    failure_policy: LocalJobFailurePolicy = field(default_factory=LocalJobFailurePolicy)
    output_dir: str = "data/local-ops/jobs"
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    updated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def __post_init__(self) -> None:
        if not self.job_id.strip():
            raise ValueError("job_id is required")
        if self.category not in JOB_CATEGORIES:
            raise ValueError("invalid local job category")
        if self.max_runtime_seconds <= 0:
            raise ValueError("max_runtime_seconds must be positive")
        if self.live_trading_enabled:
            raise ValueError("local jobs cannot enable live trading")

    def argv(self) -> list[str]:
        return [self.command, *self.args]

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "LocalJobDefinition":
        data = dict(payload)
        if isinstance(data.get("schedule"), dict):
            data["schedule"] = LocalJobSchedule(**data["schedule"])
        if isinstance(data.get("failure_policy"), dict):
            data["failure_policy"] = LocalJobFailurePolicy(**data["failure_policy"])
        return cls(**data)


@dataclass(frozen=True)
class LocalJobRun:
    run_id: str
    job_id: str
    status: str
    started_at_ms: int
    finished_at_ms: int = 0
    returncode: int | None = None
    stdout_path: str = ""
    stderr_path: str = ""
    result_path: str = ""
    artifacts: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class LocalJobResult:
    job_id: str
    run_id: str
    status: str
    returncode: int
    stdout_tail: str = ""
    stderr_tail: str = ""
    artifacts: list[str] = field(default_factory=list)
    failure_action: str = "record_only"
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def default_local_jobs() -> list[LocalJobDefinition]:
    return [
        LocalJobDefinition(
            "daily-operator-health",
            "Daily operator health",
            "Write local operator health score.",
            "operator-health-score",
            ["--json"],
            LocalJobSchedule("daily", {"time": "08:00"}),
            category="health",
        ),
        LocalJobDefinition(
            "daily-operator-report",
            "Daily operator report",
            "Write the local paper operator report.",
            "operator-report",
            ["--json"],
            LocalJobSchedule("daily", {"time": "18:00"}),
            category="report",
        ),
        LocalJobDefinition(
            "daily-evidence-manifest",
            "Daily evidence manifest",
            "Refresh local evidence manifest.",
            "evidence-manifest",
            ["--json"],
            LocalJobSchedule("daily", {"time": "18:10"}),
            category="evidence",
        ),
        LocalJobDefinition(
            "weekly-governance-report",
            "Weekly governance report",
            "Write weekly paper policy governance report.",
            "weekly-governance-report",
            ["--json"],
            LocalJobSchedule("weekly", {"weekday": "monday", "time": "09:00"}),
            category="governance",
            max_runtime_seconds=120,
        ),
        LocalJobDefinition(
            "weekly-support-verify",
            "Weekly support bundle verify",
            "Verify local support bundles.",
            "support-bundles-verify",
            ["--json"],
            LocalJobSchedule("weekly", {"weekday": "friday", "time": "16:00"}),
            category="diagnostics",
        ),
    ]


def jobs_to_json(jobs: list[LocalJobDefinition], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([job.to_dict() for job in jobs], indent=2, default=str), encoding="utf-8")
    return path
