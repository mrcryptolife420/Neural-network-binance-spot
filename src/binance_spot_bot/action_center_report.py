from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .decision_outcome_analytics import decision_outcome_analytics
from .redaction import redact_payload


def write_action_center_report(root: Path, payload: dict) -> dict[str, Any]:
    out = Path(root) / "action-center" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    decisions = list(payload.get("decisions", []))
    analytics = decision_outcome_analytics(decisions)
    report = {
        "status": "ok",
        "created_at_ms": int(time.time() * 1000),
        "daily": {
            "proposals_opened": len(payload.get("proposals", [])),
            "decisions_made": len(decisions),
            "executions_run": len(payload.get("executions", [])),
            "failed_verifications": sum(1 for item in payload.get("verifications", []) if item.get("status") == "fail"),
            "forbidden_requests_blocked": analytics["safety_blocks"],
            "unresolved_proposals": analytics["unresolved_proposals"],
        },
        "weekly": {"operator_decision_summary": analytics, "suggested_process_improvements": ["review repeated blocked proposals"]},
        "live_trading_enabled": False,
    }
    path = out / "action-center-report.json"
    md = out / "action-center-report.md"
    path.write_text(json.dumps(redact_payload(report), indent=2, default=str), encoding="utf-8")
    md.write_text(_markdown(report), encoding="utf-8")
    return {"path": str(path), "markdown": str(md), **report}


def _markdown(report: dict[str, Any]) -> str:
    daily = report["daily"]
    return "\n".join(
        [
            "# Action Center Report",
            "",
            f"Status: {report['status']}",
            f"Decisions made: {daily['decisions_made']}",
            f"Executions run: {daily['executions_run']}",
            f"Forbidden requests blocked: {daily['forbidden_requests_blocked']}",
            "",
            "Live trading enabled: false",
        ]
    )
