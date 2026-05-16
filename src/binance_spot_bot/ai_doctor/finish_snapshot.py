from __future__ import annotations

from pathlib import Path

from binance_spot_bot.portfolio_lab.common import json_write, now_ms

from .run_schema import AIDoctorFinishSnapshot


def collect_finish_snapshot(root: Path, run_id: str, status: str = "ok", exit_code: int | None = 0) -> dict[str, object]:
    snapshot = AIDoctorFinishSnapshot(run_id, now_ms(), status, exit_code)
    saved = json_write(root / "data" / "ai-doctor" / "runs" / run_id / "finish_snapshot.json", snapshot)
    return {"status": "ok", "snapshot": snapshot, "saved": saved, "live_trading_enabled": False}

