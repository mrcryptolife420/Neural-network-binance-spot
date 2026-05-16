from __future__ import annotations

from typing import Any


def build_repair_suggestions(matches: list[dict[str, Any]]) -> dict[str, Any]:
    suggestions = []
    for match in matches:
        suggestions.append({"title": match.get("recommended_fix", "investigate_first"), "severity": match.get("severity", "P3"), "why": match.get("title", ""), "safe_command": "", "manual_steps": ["inspect evidence", "patch suspect files", "run tests"], "tests_to_run": match.get("recommended_tests", ["pytest -q"]), "unsafe": False})
    return {"status": "ok", "suggestions": suggestions, "live_order_submitted": False}

