from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import now_ms, redact_value


def append_ai_doctor_event(root: Path, run_id: str, event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    event = {"ts_ms": now_ms(), "run_id": run_id, "event_type": event_type, "payload": redact_value(payload or {}), "live_trading_enabled": False}
    path = root / "data" / "ai-doctor" / "runs" / run_id / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text((path.read_text(encoding="utf-8") if path.exists() else "") + json.dumps(event, default=str) + "\n", encoding="utf-8")
    return {"status": "ok", "event": event, "path": str(path), "live_order_submitted": False}

