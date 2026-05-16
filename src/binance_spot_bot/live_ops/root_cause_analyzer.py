from __future__ import annotations

from typing import Any


def analyze_live_ops_root_cause(timeline: dict[str, Any] | None = None) -> dict[str, Any]:
    timeline = timeline or {"events": []}
    categories = [event.get("category", "") for event in timeline.get("events", [])]
    cause = "reconciliation/order state issue" if "reconciliation" in categories else "unknown/needs manual review"
    return {
        "status": "ok",
        "likely_root_cause": cause,
        "confidence": "medium" if cause != "unknown/needs manual review" else "low",
        "contributing_factors": categories,
        "unresolved_questions": [] if cause != "unknown/needs manual review" else ["manual review required"],
        "recommended_prevention_items": ["add reconciliation regression test", "keep live rearm blocked until review"],
        "required_operator_review": True,
        "live_order_submitted": False,
    }

