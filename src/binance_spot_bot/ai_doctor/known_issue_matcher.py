from __future__ import annotations

from typing import Any


def match_known_issues(errors: list[dict[str, Any]] | None = None, logs: str = "") -> dict[str, Any]:
    matches = []
    text = logs + " " + " ".join(error.get("error_type", "") + " " + error.get("message", "") for error in (errors or []))
    patterns = [
        ("streamlit_duplicate_element_id", "StreamlitDuplicateElementId", "dashboard_fix", ["src/binance_spot_bot/ui/streamlit_app.py"]),
        ("module_not_found", "ModuleNotFoundError", "dependency_fix", ["pyproject.toml"]),
        ("json_decode", "JSONDecodeError", "evidence_repair", ["data/evidence"]),
        ("secret_leak", "secret", "safety_blocker", []),
        ("stale_runner_lock", "stale runner lock", "runtime_fix", ["src/binance_spot_bot/pilot_runner.py"]),
    ]
    for issue_id, needle, task, files in patterns:
        if needle.lower() in text.lower():
            matches.append({"issue_id": issue_id, "title": needle, "severity": "P1" if issue_id == "secret_leak" else "P2", "confidence": "high", "suspect_files": files, "recommended_fix": task, "recommended_tests": ["python -m compileall -q src tests", "pytest -q"], "safety_notes": ["do not start live trading", "do not expose secrets"]})
    if not matches:
        matches.append({"issue_id": "unknown_investigate_first", "title": "Unknown issue", "severity": "P3", "confidence": "low", "suspect_files": [], "recommended_fix": "investigate_first", "recommended_tests": ["pytest -q"], "safety_notes": ["collect more evidence"]})
    return {"status": "ok", "matches": matches, "live_order_submitted": False}

