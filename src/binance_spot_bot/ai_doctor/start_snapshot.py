from __future__ import annotations

from pathlib import Path

from binance_spot_bot.portfolio_lab.common import json_write

from .run_schema import AIDoctorStartSnapshot, create_default_run


def collect_start_snapshot(root: Path, profile_id: str = "paper") -> dict[str, object]:
    run = create_default_run(root, profile_id)
    snapshot = AIDoctorStartSnapshot(run.run_id, run.started_at_ms, str(root), run.python_version, run.platform, run.safe_env)
    saved = json_write(root / "data" / "ai-doctor" / "runs" / run.run_id / "start_snapshot.json", snapshot)
    return {"status": "ok", "run": run, "snapshot": snapshot, "saved": saved, "live_trading_enabled": False}

