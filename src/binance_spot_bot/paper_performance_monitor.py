from __future__ import annotations

from typing import Any


def paper_performance_monitor(rows: list[dict[str, Any]], *, min_pnl_quote: float = -10.0, max_drawdown_quote: float = 25.0) -> dict[str, Any]:
    pnl = sum(float(row.get("pnl", row.get("pnl_quote", 0.0)) or 0.0) for row in rows)
    drawdown = max((abs(float(row.get("drawdown", row.get("drawdown_quote", 0.0)) or 0.0)) for row in rows), default=0.0)
    status = "ok" if pnl >= min_pnl_quote and drawdown <= max_drawdown_quote else "warn"
    return {"status": status, "pnl_quote": pnl, "max_drawdown_quote": drawdown, "rows": len(rows), "live_trading_enabled": False}
