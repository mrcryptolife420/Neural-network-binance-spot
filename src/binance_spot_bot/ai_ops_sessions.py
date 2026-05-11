from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def write_ai_ops_session(root: Path, question: str, answer: dict[str, Any]) -> Path:
    out = Path(root) / "ai-ops" / "sessions"
    out.mkdir(parents=True, exist_ok=True)
    payload = redact_payload(
        {
            "question": question,
            "answer": answer,
            "sources": answer.get("sources", []),
            "safety_decisions": answer.get("intent", {}),
            "command_proposals": answer.get("command_proposal"),
            "timestamp_ms": int(time.time() * 1000),
            "live_trading_enabled": False,
        }
    )
    path = out / "latest-session.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path
