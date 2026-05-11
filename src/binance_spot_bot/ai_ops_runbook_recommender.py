from __future__ import annotations

from typing import Any

from .operator_runbooks import get_runbook


def recommend_runbook(question: str) -> dict[str, Any]:
    q = question.lower()
    if "dashboard" in q or "smoke" in q:
        runbook_id = "browser-smoke-failed"
    elif "evidence" in q or "ontbreekt" in q:
        runbook_id = "evening-review"
    elif "governance" in q or "policy" in q:
        runbook_id = "policy-challenger-failed"
    elif "support" in q or "job" in q or "failed" in q:
        runbook_id = "failed-scheduled-report"
    else:
        runbook_id = "morning-check"
    runbook = get_runbook(runbook_id)
    return {
        "status": "ready",
        "runbook": runbook_id,
        "matching_reason": f"matched local question to {runbook_id}",
        "first_steps": [step.title for step in runbook.steps[:3]],
        "expected_artifacts": ["local report", "support bundle or evidence manifest"],
        "urgency": "warning" if runbook_id != "morning-check" else "info",
        "safe_commands": [step.command for step in runbook.steps if step.command],
        "sources": ["operator_runbooks"],
        "live_trading_enabled": False,
    }
