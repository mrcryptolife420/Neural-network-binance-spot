from __future__ import annotations

from decimal import Decimal
from typing import Any

from binance_spot_bot.redaction import redact_payload
from . import NO_LIVE_STATEMENT


def evaluate_research_guards(results: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    blockers = []
    for row in results:
        checks = []
        if int(row.get("candle_count", 0)) < 20:
            checks.append({"guard": "minimum_candle_count", "status": "warn"})
        if int(row.get("fill_count", 0)) < 2:
            checks.append({"guard": "too_few_trades", "status": "warn"})
        if abs(Decimal(str(row.get("max_drawdown", "0")))) > Decimal("5"):
            checks.append({"guard": "excessive_drawdown", "status": "block"})
        if Decimal(str(row.get("paper_pnl", "0"))) > Decimal("100"):
            checks.append({"guard": "suspicious_perfect_score", "status": "warn"})
        if any(item["status"] == "block" for item in checks):
            blockers.append(str(row.get("job_id")))
        rows.append({"job_id": row.get("job_id"), "symbol": row.get("symbol"), "checks": checks or [{"guard": "baseline", "status": "pass"}]})
    return redact_payload({"status": "ok" if not blockers else "blocked", "guards": rows, "blockers": blockers, "no_live_statement": NO_LIVE_STATEMENT, "live_trading_enabled": False})
