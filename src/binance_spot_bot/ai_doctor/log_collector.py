from __future__ import annotations

from pathlib import Path

from binance_spot_bot.portfolio_lab.common import json_write, redact_value


def collect_recent_logs(root: Path, run_id: str, logs: list[str] | None = None, max_chars: int = 4000) -> dict[str, object]:
    safe_logs = [str(redact_value(item))[:max_chars] for item in (logs or ["AI Doctor fixture log: dashboard started in safe mode"])]
    run_root = root / "data" / "ai-doctor" / "runs" / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "recent_logs.txt").write_text("\n".join(safe_logs), encoding="utf-8")
    saved = json_write(run_root / "log_index.json", {"logs": [{"name": "fixture", "chars": len(safe_logs[0])}], "missing_warnings": []})
    return {"status": "ok", "saved": saved, "live_trading_enabled": False}

