from __future__ import annotations

import json
from typing import Any

from .ai_ops_answer import answer_ai_ops_query
from .ai_ops_sessions import write_ai_ops_session
from .config import BotSettings
from .redaction import redact_payload


def answer_ops_question(settings: BotSettings, question: str) -> dict[str, Any]:
    answer = answer_ai_ops_query(question, root=settings.data_dir)
    if "answer" not in answer:
        answer["answer"] = answer.get("summary", "")
    answer.setdefault("sources", answer.get("evidence", []))
    return redact_payload(answer)


def write_ops_assistant_answer(settings: BotSettings, question: str) -> dict[str, Any]:
    payload = answer_ops_question(settings, question)
    out = settings.data_dir / "ops-assistant"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "latest-answer.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    session_path = write_ai_ops_session(settings.data_dir, question, payload)
    return {"path": str(path), "session": str(session_path), **payload}
