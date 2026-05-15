from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload

QUERY_SCOPES = {
    "runtime_snapshot",
    "candles",
    "equity_points",
    "signals",
    "fills",
    "risk_blocks",
    "alerts",
    "sessions",
    "model_status",
    "portfolio_status",
    "operator_evidence",
    "support_status",
    "performance_metrics",
}


def demo_analytics_snapshot() -> dict[str, Any]:
    return {
        "mode": "demo",
        "symbol": "BTCUSDT",
        "candles": [{"symbol": "BTCUSDT", "close": 100 + idx, "timestamp_ms": idx * 60_000} for idx in range(20)],
        "equity": [{"value": 1000 + idx, "timestamp_ms": idx * 60_000} for idx in range(20)],
        "signals": [{"symbol": "BTCUSDT", "confidence": idx / 20, "timestamp_ms": idx * 60_000} for idx in range(20)],
        "fills": [{"symbol": "BTCUSDT", "side": "BUY" if idx % 2 == 0 else "SELL", "qty": "0.01"} for idx in range(4)],
        "alerts": [{"severity": "info", "message": "demo alert"}],
        "risk_blocks": [{"reason": "daily_loss_guard", "blocked": False}],
        "active_model": {"model_version": "demo-model"},
        "portfolio": {"exposure_quote": "0"},
        "performance": {"payload_bytes": 1024},
    }


def _items_for_scope(snapshot: dict[str, Any], scope: str) -> Any:
    mapping = {
        "runtime_snapshot": snapshot,
        "candles": snapshot.get("candles", []),
        "equity_points": snapshot.get("equity", snapshot.get("equity_points", [])),
        "signals": snapshot.get("signals", []),
        "fills": snapshot.get("fills", []),
        "risk_blocks": snapshot.get("risk_blocks", snapshot.get("block_reasons", [])),
        "alerts": snapshot.get("alerts", []),
        "sessions": snapshot.get("recent_sessions", snapshot.get("sessions", [])),
        "model_status": snapshot.get("active_model", snapshot.get("model_status", {})),
        "portfolio_status": snapshot.get("portfolio", snapshot.get("portfolio_status", {})),
        "operator_evidence": snapshot.get("operator_evidence", {}),
        "support_status": snapshot.get("support_status", {}),
        "performance_metrics": snapshot.get("performance", snapshot.get("meta", {})),
    }
    return mapping[scope]


def analytics_query(
    snapshot: dict[str, Any] | None = None,
    *,
    scope: str = "runtime_snapshot",
    tail: int = 250,
    symbol: str = "",
    mode: str = "",
    severity: str = "",
    aggregation: str = "none",
    downsample: int = 1,
    max_payload_bytes: int = 250_000,
) -> dict[str, Any]:
    if scope not in QUERY_SCOPES:
        return {"status": "blocked", "blockers": [f"unknown scope: {scope}"], "live_trading_enabled": False}
    snapshot = snapshot or demo_analytics_snapshot()
    if snapshot.get("mode") == "live" or mode == "live":
        return {"status": "blocked", "blockers": ["live mode blocked"], "live_trading_enabled": False}
    data = _items_for_scope(snapshot, scope)
    if isinstance(data, list):
        rows = data
        if symbol:
            rows = [item for item in rows if not isinstance(item, dict) or item.get("symbol", symbol).upper() == symbol.upper()]
        if severity:
            rows = [item for item in rows if not isinstance(item, dict) or item.get("severity") == severity]
        if downsample > 1:
            rows = rows[::downsample]
        rows = rows[-max(1, min(tail, 1000)) :]
        data = rows
    if aggregation == "count" and isinstance(data, list):
        data = {"count": len(data)}
    payload = redact_dashboard_payload(
        {
            "status": "ok",
            "scope": scope,
            "data": data,
            "tail": tail,
            "aggregation": aggregation,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )
    size = len(str(payload).encode("utf-8"))
    if size > max_payload_bytes:
        return {"status": "blocked", "blockers": ["payload size limit exceeded"], "payload_bytes": size, "live_trading_enabled": False}
    payload["payload_bytes"] = size
    return payload
