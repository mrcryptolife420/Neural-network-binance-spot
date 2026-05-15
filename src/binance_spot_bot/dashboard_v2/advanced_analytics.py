from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .analytics_query import demo_analytics_snapshot
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def advanced_analytics_report(snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    snapshot = snapshot or demo_analytics_snapshot()
    equity = snapshot.get("equity", [])
    fills = snapshot.get("fills", [])
    signals = snapshot.get("signals", [])
    alerts = snapshot.get("alerts", [])
    values = [float(item.get("value", 0)) for item in equity if isinstance(item, dict)]
    max_drawdown = 0.0
    peak = values[0] if values else 0.0
    for value in values:
        peak = max(peak, value)
        max_drawdown = min(max_drawdown, value - peak)
    payload = {
        "status": "ok",
        "session_pnl_distribution": {"points": len(values), "start": values[0] if values else None, "end": values[-1] if values else None},
        "equity_drawdown": {"max_drawdown_quote": max_drawdown},
        "fill_quality_summary": {"fills": len(fills)},
        "risk_block_heatmap": {"blocks": len(snapshot.get("risk_blocks", []))},
        "signal_confidence_trend": {"signals": len(signals), "avg_confidence": sum(float(item.get("confidence", 0)) for item in signals) / max(1, len(signals))},
        "data_quality_warnings_trend": {"alerts": len(alerts)},
        "market_data_latency_reconnects": {"reconnects": 0},
        "demo_pilot_counters": {"orders": len(snapshot.get("open_demo_orders", []))},
        "model_status_summary": snapshot.get("active_model", {}),
        "portfolio_exposure_summary": snapshot.get("portfolio", {}),
        "operator_evidence_status": snapshot.get("operator_evidence", {}),
        "support_bundle_health": snapshot.get("support_status", {}),
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }
    return redact_dashboard_payload(payload)


def write_advanced_analytics_report(root: Path | str = ".", snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    out = Path(root) / "data" / "dashboard-v2" / "analytics"
    out.mkdir(parents=True, exist_ok=True)
    payload = advanced_analytics_report(snapshot)
    json_path = out / "advanced-analytics.json"
    md_path = out / "advanced-analytics.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "# Dashboard V2 Advanced Analytics\n\n"
        f"Status: {payload['status']}\n"
        f"No-live proof: {payload['no_live_statement']}\n",
        encoding="utf-8",
    )
    return {"status": "ok", "json": str(json_path), "markdown": str(md_path), "report": payload, "live_trading_enabled": False}
