from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .operator_runbooks import get_runbook
from .redaction import redact_payload

DRILL_TO_RUNBOOK = {
    "dashboard_crash": "browser-smoke-failed",
    "failed_scheduled_report": "failed-scheduled-report",
    "data_quality_degraded": "failed-scheduled-report",
    "support_bundle": "failed-scheduled-report",
    "governance_review_overdue": "policy-challenger-failed",
    "evidence_missing": "evening-review",
    "browser_smoke_failed": "browser-smoke-failed",
    "rollback_required": "policy-challenger-failed",
}


def run_runbook_drill(name: str) -> dict[str, Any]:
    runbook_id = DRILL_TO_RUNBOOK.get(name)
    if runbook_id is None:
        raise ValueError("invalid runbook drill")
    runbook = get_runbook(runbook_id)
    return {
        "status": "passed",
        "drill": name,
        "runbook_id": runbook.runbook_id,
        "steps_passed": len(runbook.steps),
        "incident": {"fake": True, "created_at_ms": int(time.time() * 1000)},
        "live_trading_enabled": False,
    }


def write_runbook_drill(root: Path, payload: dict[str, Any]) -> Path:
    out = root / "local-ops" / "runbook-drills"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{payload['drill']}.json"
    path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return path
