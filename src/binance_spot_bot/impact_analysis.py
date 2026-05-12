from __future__ import annotations

from typing import Any

from .code_ownership import build_code_ownership
from .test_impact_map import select_tests_for_changes


def _risk_score(path: str) -> int:
    lower = path.lower()
    if any(token in lower for token in ["security", "redaction", "credentials", "live", "order", "migration", "restore"]):
        return 90
    if any(token in lower for token in ["runtime", "execution", "risk", "cli.py"]):
        return 70
    if any(token in lower for token in ["ui/", "dashboard", "streamlit"]):
        return 50
    if any(token in lower for token in ["docs/", "roadmap docs"]):
        return 25
    return 40


def impact_analysis(changed: list[str]) -> dict[str, Any]:
    scores = [_risk_score(path) for path in changed] or [0]
    score = max(scores)
    level = "critical" if score >= 85 else "high" if score >= 65 else "medium" if score >= 40 else "low"
    tests = select_tests_for_changes(changed, strict=level in {"high", "critical"})
    owners = build_code_ownership(changed)
    payload = {
        "status": "ready",
        "changed": changed,
        "risk": {"payload": {"score": score, "level": level}},
        "tests": tests["payload"],
        "ownership": owners["payload"],
        "impacted_docs": ["docs/impact-analysis.md"] if changed else [],
        "required_validation_commands": tests["payload"]["tests"],
        "release_notes_sections": sorted({item["owner"] for item in owners["payload"]["files"]}),
        "no_live_blockers": [],
        "live_trading_enabled": False,
    }
    return payload
