from __future__ import annotations

from typing import Any


def evaluate_demo_dataset_quality_v2(vault_report: dict[str, Any], target_report: dict[str, Any], burndown: dict[str, Any]) -> dict[str, Any]:
    blockers = []
    if vault_report.get("status") == "blocked":
        blockers.append("vault integrity blocked")
    if target_report.get("progress_percent", 0) < 70:
        blockers.append("demo coverage too low")
    if any(item.get("priority") == "DQ-P0" for item in burndown.get("issues", [])):
        blockers.append("P0 data quality issue")
    score = max(0.0, min(100.0, float(target_report.get("progress_percent", 0)) - len(blockers) * 30))
    grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 65 else "D" if score >= 40 else "F"
    return {"status": "blocked" if blockers or grade in {"D", "F"} else "ok", "quality_score": score, "grade": grade, "blockers": blockers, "burndown_status": burndown.get("status"), "live_execution_enabled": False, "live_trading_enabled": False}

