from __future__ import annotations

from typing import Any

from .ai_ops_answer import answer_ai_ops_query
from .redaction import redact_payload


def local_ai_ops_answer(question: str, *, mode: str = "rules_only", context: dict[str, Any] | None = None) -> dict[str, Any]:
    if mode == "remote_llm":
        return {"status": "blocked", "reason": "remote_llm_disabled_by_default", "live_trading_enabled": False}
    answer = answer_ai_ops_query(question, context=context)
    return redact_payload({**answer, "mode": mode, "tools_enabled": False, "live_trading_enabled": False})
