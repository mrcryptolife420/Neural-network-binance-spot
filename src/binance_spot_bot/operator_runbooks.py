from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .local_job_allowlist import validate_local_job_command
from .redaction import redact_payload


@dataclass(frozen=True)
class RunbookStep:
    title: str
    command: str = ""
    expected_output: str = ""
    done: bool = False


@dataclass(frozen=True)
class OperatorRunbook:
    runbook_id: str
    title: str
    trigger: str
    severity: str
    steps: list[RunbookStep]
    escalation: str = "manual_review"
    done_criteria: str = "All steps completed and evidence written."
    safety_notes: str = "Local paper operations only. Live trading remains disabled."
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def default_runbooks() -> list[OperatorRunbook]:
    return [
        OperatorRunbook("morning-check", "Morning check", "daily_start", "info", [RunbookStep("Run health score", "operator-health-score --json", "status ok or warn"), RunbookStep("Review local ops snapshot", "local-ops-snapshot --json", "snapshot generated")]),
        OperatorRunbook("evening-review", "Evening review", "daily_end", "info", [RunbookStep("Generate operator report", "operator-report --json", "report path"), RunbookStep("Refresh evidence manifest", "evidence-manifest --json", "manifest path")]),
        OperatorRunbook("failed-scheduled-report", "Failed scheduled report", "job_failed", "warning", [RunbookStep("Run diagnostics", "diagnostics --json", "diagnostics generated"), RunbookStep("Create support bundle", "support-bundle --json", "bundle path")]),
        OperatorRunbook("policy-challenger-failed", "Policy challenger failed", "governance_stop", "warning", [RunbookStep("Run governance simulation", "governance-simulation --case policy_violation --json", "suspend decision"), RunbookStep("Write weekly governance report", "weekly-governance-report --json", "report path")]),
        OperatorRunbook("browser-smoke-failed", "Browser smoke failed", "dashboard_smoke_failed", "warning", [RunbookStep("Run dashboard smoke", "dashboard-smoke --seconds 1", "status ok"), RunbookStep("Create support bundle", "support-bundle --json", "bundle path")]),
    ]


def runbook_index() -> dict[str, Any]:
    return {"status": "ready", "runbooks": [book.to_dict() for book in default_runbooks()], "live_trading_enabled": False}


def get_runbook(runbook_id: str) -> OperatorRunbook:
    for book in default_runbooks():
        if book.runbook_id == runbook_id:
            return book
    raise KeyError(runbook_id)


def export_runbooks(root: Path) -> dict[str, str]:
    out = root / "local-ops" / "runbooks"
    out.mkdir(parents=True, exist_ok=True)
    payload = runbook_index()
    json_path = out / "runbooks.json"
    md_path = out / "runbooks.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(_runbook_markdown(payload["runbooks"]), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "live_trading_enabled": "false"}


def validate_runbook_commands(runbook: OperatorRunbook) -> dict[str, Any]:
    blocked = []
    for step in runbook.steps:
        if step.command and not validate_local_job_command(step.command).allowed:
            blocked.append(step.command)
    return {"status": "ok" if not blocked else "blocked", "blocked": blocked, "live_trading_enabled": False}


def _runbook_markdown(runbooks: list[dict[str, Any]]) -> str:
    lines = ["# Local Paper Operator Runbooks", "", "Live trading: disabled", ""]
    for book in runbooks:
        lines.extend([f"## {book['title']}", "", f"Trigger: {book['trigger']}", f"Severity: {book['severity']}", ""])
        for step in book["steps"]:
            cmd = f" `{step['command']}`" if step.get("command") else ""
            lines.append(f"- {step['title']}{cmd}")
        lines.append("")
    return "\n".join(lines)
