from __future__ import annotations

import re
from typing import Any


def roadmap_quality_score(text: str) -> dict[str, Any]:
    categories = {
        "completeness": bool(re.search(r"Definition of Done", text, re.IGNORECASE)),
        "phase_clarity": bool(re.search(r"Fase|PR \d+", text, re.IGNORECASE)),
        "test_coverage_clarity": bool(re.search(r"Tests|Validatie", text, re.IGNORECASE)),
        "evidence_clarity": bool(re.search(r"evidence|bewijs", text, re.IGNORECASE)),
        "safety_clarity": bool(re.search(r"Geen live trading|no-live|live trading.*disabled", text, re.IGNORECASE)),
        "file_boundary_clarity": bool(re.search(r"src/|tests/|docs/", text, re.IGNORECASE)),
        "dependency_clarity": bool(re.search(r"Volgt op|depends|dependency", text, re.IGNORECASE)),
        "execution_readiness": bool(re.search(r"Beste eerste Codex|CLI command|python -m", text, re.IGNORECASE)),
    }
    blockers = [name for name, ok in categories.items() if not ok]
    score = round(100 * sum(1 for ok in categories.values() if ok) / len(categories))
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D"
    if blockers:
        grade = "F" if {"safety_clarity", "test_coverage_clarity", "completeness"} & set(blockers) else grade
    return {"status": "blocked" if grade == "F" else "ready", "score": score, "grade": grade, "categories": categories, "blockers": blockers, "live_trading_enabled": False}
