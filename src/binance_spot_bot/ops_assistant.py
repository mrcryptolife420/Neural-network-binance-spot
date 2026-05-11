from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import BotSettings
from .operator_ops import artifact_catalog, local_ops_snapshot, operator_health_score
from .redaction import redact_payload


BLOCKED_TERMS = {"place order", "market buy", "market sell", "withdraw", "disable kill", "live trading"}


def answer_ops_question(settings: BotSettings, question: str) -> dict[str, Any]:
    normalized = question.lower()
    if any(term in normalized for term in BLOCKED_TERMS):
        return {
            "status": "blocked",
            "answer": "Ik kan alleen lokale demo/paper status uitleggen en geen live orders of withdrawal acties uitvoeren.",
            "sources": [],
            "live_trading_enabled": False,
        }
    snapshot = local_ops_snapshot(settings)
    health = operator_health_score(settings)
    catalog = artifact_catalog(settings, limit=25)
    sources = [
        {"name": "local_ops_snapshot", "status": snapshot.get("status")},
        {"name": "operator_health_score", "status": health.get("status")},
        {"name": "artifact_catalog", "items": len(catalog.get("items", []))},
    ]
    focus = "dashboard" if "dashboard" in normalized else "bot" if "bot" in normalized else "ops"
    answer = {
        "dashboard": f"Dashboard status is {snapshot.get('status', 'unknown')}; check stale artifacts before relying on visuals.",
        "bot": f"Bot health score is {health.get('score', 0)} with status {health.get('status', 'unknown')}.",
        "ops": f"Local ops status is {snapshot.get('status', 'unknown')} with {len(catalog.get('items', []))} cataloged artifacts.",
    }[focus]
    return redact_payload({"status": "answered", "answer": answer, "sources": sources, "live_trading_enabled": False})


def write_ops_assistant_answer(settings: BotSettings, question: str) -> dict[str, Any]:
    payload = answer_ops_question(settings, question)
    out = settings.data_dir / "ops-assistant"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "latest-answer.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return {"path": str(path), **payload}
