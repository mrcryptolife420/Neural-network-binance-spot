from __future__ import annotations

from typing import Any

from .metrics_schema import MetricEvent


def paper_performance_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pnl = sum(float(row.get("pnl", row.get("pnl_quote", 0))) for row in rows)
    drawdown = max([float(row.get("drawdown", 0)) for row in rows] or [0.0])
    fills = sum(int(row.get("fills", row.get("fill_count", 0))) for row in rows)
    blocked = sum(int(row.get("blocked_trades", row.get("blocked", 0))) for row in rows)
    alerts = sum(int(row.get("alerts", 0)) for row in rows)
    events = [
        MetricEvent("paper.pnl", pnl, source="paper-session", category="paper_performance", unit="quote"),
        MetricEvent("paper.drawdown", drawdown, source="paper-session", category="paper_performance", unit="pct", status="warn" if drawdown > 10 else "ok"),
        MetricEvent("paper.fills", float(fills), source="paper-session", category="paper_performance"),
        MetricEvent("paper.blocked_trades", float(blocked), source="paper-session", category="paper_performance"),
        MetricEvent("paper.alerts", float(alerts), source="paper-session", category="incident", status="warn" if alerts else "ok"),
    ]
    return {"status": "warn" if drawdown > 10 or alerts else "ok", "observations": len(rows), "pnl": pnl, "drawdown": drawdown, "events": [event.to_dict() for event in events], "live_trading_enabled": False}
