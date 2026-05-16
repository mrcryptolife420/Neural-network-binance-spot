from __future__ import annotations

from typing import Any


def check_recovery_readiness(*, classification: dict[str, Any] | None = None, drill: dict[str, Any] | None = None, root_cause: dict[str, Any] | None = None) -> dict[str, Any]:
    classification = classification or {"severity": "P1", "blockers": ["live_rearm_blocked"]}
    drill = drill or {"status": "passed"}
    root_cause = root_cause or {"required_operator_review": True}
    blockers = []
    if classification.get("severity") in {"P0", "P1"}:
        blockers.append("P0/P1 incident requires operator review")
    if drill.get("status") != "passed":
        blockers.append("rollback drill required")
    if root_cause.get("required_operator_review"):
        blockers.append("root cause review required")
    state = "live_rearm_blocked" if blockers else "safe_to_resume_paper_or_demo"
    return {"status": state, "blockers": blockers, "live_rearm_allowed": False, "paper_or_demo_resume_allowed": not blockers, "live_order_submitted": False, "live_rearmed": False}

