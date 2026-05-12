from __future__ import annotations

from typing import Any

from .impact_analysis import impact_analysis


def repo_knowledge_codex_task_hints(changed: list[str]) -> dict[str, Any]:
    impact = impact_analysis(changed)
    return {
        "status": "ready",
        "allowed_files": changed,
        "required_tests": impact["required_validation_commands"],
        "forbidden_files": [".env", "*.pem", "data/secrets/*"],
        "safety_constraints": ["local-only", "no live trading", "no signed/order/account endpoints"],
        "reviewer_role": impact["risk"]["payload"]["level"],
        "release_notes_sections": impact["release_notes_sections"],
        "live_trading_enabled": False,
    }


def repo_knowledge_codex_prompt(topic: str) -> dict[str, Any]:
    return {"status": "ready", "topic": topic, "prompt": f"Use repository knowledge for {topic}; keep live trading disabled.", "live_trading_enabled": False}
