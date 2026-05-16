from __future__ import annotations

from typing import Any


def analyze_walk_forward_performance(rolling_report: dict[str, Any]) -> dict[str, Any]:
    results = rolling_report.get("results", [])
    pnls = [float(row.get("validation_paper_pnl", 0.0)) for row in results]
    drawdowns = [float(row.get("max_drawdown", 0.0)) for row in results]
    pass_count = len([row for row in results if float(row.get("max_drawdown", 0.0)) < 0.08])
    total = len(results) or 1
    return {
        "status": "ok",
        "window_count": len(results),
        "pass_window_ratio": round(pass_count / total, 6),
        "worst_window_pnl": round(min(pnls) if pnls else 0.0, 6),
        "best_window_pnl": round(max(pnls) if pnls else 0.0, 6),
        "median_window_pnl": round(sorted(pnls)[len(pnls) // 2] if pnls else 0.0, 6),
        "worst_window_drawdown": round(max(drawdowns) if drawdowns else 0.0, 6),
        "overfit_gap_proxy": round((max(pnls) - min(pnls)) if pnls else 0.0, 6),
        "rebalance_event_count": sum(len(row.get("rebalance_events", [])) for row in results),
        "live_trading_enabled": False,
    }

