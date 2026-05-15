from __future__ import annotations

from typing import Any


def next_roadmap_recommendation(audit: dict[str, Any] | None = None) -> dict[str, Any]:
    audit = audit or {}
    blockers = audit.get("blockers", [])
    warnings = audit.get("warnings", [])
    if blockers:
        title = "Roadmap 101 - Paper OS Stabilization Sprint, Blocker Burn-Down & Reliability Hardening"
        focus = "blocker burn-down"
    elif warnings:
        title = "Roadmap 101 - Paper OS Stabilization Sprint, Warning Burn-Down & Operator Acceptance"
        focus = "warning burn-down"
    else:
        title = "Roadmap 101 - Paper OS Stabilization Sprint, Reliability Hardening & Operator Acceptance"
        focus = "reliability hardening"
    return {
        "recommended_number": "101",
        "recommended_title": title,
        "rationale": "Roadmap 100 is a paper-only milestone; the next step should stabilize any audit gaps before new feature expansion.",
        "top_blockers": blockers[:5],
        "warnings": warnings[:5],
        "subsystem_focus": focus,
        "codex_first_task": "Run the Roadmap 100 audit bundle, list blockers, then implement the smallest reliability fixes first.",
        "no_live_constraints": ["do not add live trading", "do not add signed real-order execution", "keep demo/paper/testnet-readiness separated"],
        "live_trading_enabled": False,
    }
