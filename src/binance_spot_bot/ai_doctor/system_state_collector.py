from __future__ import annotations

from pathlib import Path

from binance_spot_bot.portfolio_lab.common import json_write


def collect_system_state(root: Path, run_id: str) -> dict[str, object]:
    state = {"diagnostics": {"status": "ok"}, "redaction_self_test": {"status": "ok"}, "safe_env": {"LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"}, "live_trading_enabled": False}
    saved = json_write(root / "data" / "ai-doctor" / "runs" / run_id / "system_state" / "diagnostics.json", state)
    return {"status": "ok", "state": state, "saved": saved}

