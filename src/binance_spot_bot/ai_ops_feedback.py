from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def record_ai_ops_feedback(rating: int, note: str = "", *, root: Path | None = None) -> dict[str, Any]:
    payload = redact_payload({"status": "recorded", "rating": rating, "note": note, "timestamp_ms": int(time.time() * 1000), "live_trading_enabled": False})
    if root is not None:
        out = Path(root) / "ai-ops" / "feedback"
        out.mkdir(parents=True, exist_ok=True)
        with (out / "feedback.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=str) + "\n")
    return payload
