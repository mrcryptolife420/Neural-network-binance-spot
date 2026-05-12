from __future__ import annotations

from pathlib import Path
from typing import Any

from .repo_inventory import build_repo_inventory


def detect_refactor_candidates(root: Path | str = ".", line_threshold: int = 700) -> dict[str, Any]:
    inventory = build_repo_inventory(root)["payload"]["files"]
    candidates = []
    for item in inventory:
        if item["category"] == "source" and item["line_count"] > line_threshold:
            candidates.append({"candidate_id": item["path"], "module": item["path"], "reason": "large_module", "impact": "medium", "suggested_split": "extract cohesive service/helpers", "required_tests": ["python -m pytest -q"], "risk_level": "medium"})
        if item["path"].endswith("cli.py") or item["path"].endswith("streamlit_app.py"):
            candidates.append({"candidate_id": item["path"], "module": item["path"], "reason": "high_complexity_surface", "impact": "high", "suggested_split": "keep facade and move command/panel handlers to owner modules", "required_tests": ["check-all", "dashboard-smoke"], "risk_level": "high"})
    return {"status": "ready", "candidates": candidates, "live_trading_enabled": False}


def refactor_candidates(files: list[str]) -> dict[str, Any]:
    candidates = [{"module": path, "reason": "provided_for_review"} for path in files]
    return {"status": "ready", "candidates": candidates, "live_trading_enabled": False}
