from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

import plotly.graph_objects as go

from binance_spot_bot.types import Candle


def _dt(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def candlestick_figure(
    candles: list[Candle],
    signals: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    open_orders: list[dict[str, Any]] | None = None,
    reconciliation_events: list[dict[str, Any]] | None = None,
) -> go.Figure:
    fig = go.Figure()
    if candles:
        fig.add_trace(
            go.Candlestick(
                x=[_dt(c.open_time_ms) for c in candles],
                open=[float(c.open) for c in candles],
                high=[float(c.high) for c in candles],
                low=[float(c.low) for c in candles],
                close=[float(c.close) for c in candles],
                name="Candles",
            )
        )
    buy_signals = [s for s in signals if s.get("side") == "BUY"]
    sell_signals = [s for s in signals if s.get("side") == "SELL"]
    if buy_signals:
        fig.add_trace(
            go.Scatter(
                x=[_dt(int(s["timestamp_ms"])) for s in buy_signals],
                y=[float(Decimal(str(s["price"]))) for s in buy_signals],
                mode="markers",
                marker={"symbol": "triangle-up", "size": 10, "color": "#1f9d55"},
                name="BUY signal",
            )
        )
    if sell_signals:
        fig.add_trace(
            go.Scatter(
                x=[_dt(int(s["timestamp_ms"])) for s in sell_signals],
                y=[float(Decimal(str(s["price"]))) for s in sell_signals],
                mode="markers",
                marker={"symbol": "triangle-down", "size": 10, "color": "#d64545"},
                name="SELL signal",
            )
        )
    if fills:
        fig.add_trace(
            go.Scatter(
                x=[_dt(int(f["timestamp_ms"])) for f in fills],
                y=[float(Decimal(str(f["price"]))) for f in fills],
                mode="markers",
                marker={"symbol": "circle", "size": 9, "color": "#2563eb"},
                name="Paper fills",
            )
        )
    order_points = _order_points(open_orders or [], candles)
    if order_points:
        fig.add_trace(
            go.Scatter(
                x=[point["x"] for point in order_points],
                y=[point["y"] for point in order_points],
                text=[point["text"] for point in order_points],
                mode="markers",
                marker={"symbol": "diamond", "size": 10, "color": "#f59e0b"},
                name="Open demo orders",
            )
        )
    reconciliation_points = _reconciliation_points(reconciliation_events or [], candles)
    if reconciliation_points:
        fig.add_trace(
            go.Scatter(
                x=[point["x"] for point in reconciliation_points],
                y=[point["y"] for point in reconciliation_points],
                text=[point["text"] for point in reconciliation_points],
                mode="markers",
                marker={"symbol": "x", "size": 10, "color": "#7c3aed"},
                name="Reconciliation",
            )
        )
    fig.update_layout(
        height=520,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        xaxis_rangeslider_visible=False,
        legend_orientation="h",
        template="plotly_white",
    )
    return fig


def _fallback_time(candles: list[Candle]) -> int:
    return candles[-1].close_time_ms if candles else 0


def _fallback_price(candles: list[Candle]) -> float:
    return float(candles[-1].close) if candles else 0.0


def _order_points(rows: list[dict[str, Any]], candles: list[Candle]) -> list[dict[str, Any]]:
    points = []
    fallback_time = _fallback_time(candles)
    fallback_price = _fallback_price(candles)
    for row in rows:
        if row.get("status") == "error":
            continue
        timestamp = int(row.get("timestamp_ms") or row.get("time") or fallback_time)
        price = row.get("price") or row.get("stopPrice") or fallback_price
        points.append(
            {
                "x": _dt(timestamp),
                "y": float(Decimal(str(price))),
                "text": str(row.get("clientOrderId") or row.get("orderId") or "open order"),
            }
        )
    return points


def _reconciliation_points(rows: list[dict[str, Any]], candles: list[Candle]) -> list[dict[str, Any]]:
    points = []
    timestamp = _fallback_time(candles)
    price = _fallback_price(candles)
    for row in rows:
        point_time = int(row.get("checked_at_ms") or row.get("timestamp_ms") or timestamp)
        points.append({"x": _dt(point_time), "y": price, "text": str(row.get("type") or row.get("status") or "reconciliation")})
    return points


def equity_figure(points: list[dict[str, Any]]) -> go.Figure:
    fig = go.Figure()
    if points:
        fig.add_trace(
            go.Scatter(
                x=[_dt(int(p["timestamp_ms"])) for p in points],
                y=[float(Decimal(str(p["equity"]))) for p in points],
                mode="lines",
                name="Paper equity",
                line={"color": "#2563eb", "width": 2},
            )
        )
    fig.update_layout(
        height=260,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        template="plotly_white",
    )
    return fig


def runner_heartbeat_figure(rows: list[dict[str, Any]]) -> go.Figure:
    fig = go.Figure()
    points = [row for row in rows if row.get("timestamp_ms")]
    if points:
        fig.add_trace(
            go.Scatter(
                x=[_dt(int(row["timestamp_ms"])) for row in points],
                y=[float(Decimal(str(row.get("heartbeat_age_ms", 0)))) for row in points],
                mode="lines+markers",
                name="Heartbeat age ms",
                line={"color": "#2563eb", "width": 2},
            )
        )
    fig.update_layout(height=220, margin={"l": 10, "r": 10, "t": 30, "b": 10}, template="plotly_white")
    return fig


def runner_equity_pnl_figure(rows: list[dict[str, Any]]) -> go.Figure:
    fig = go.Figure()
    points = [row for row in rows if row.get("timestamp_ms")]
    if points:
        fig.add_trace(
            go.Scatter(
                x=[_dt(int(row["timestamp_ms"])) for row in points],
                y=[float(Decimal(str(row.get("equity", 0)))) for row in points],
                mode="lines",
                name="Equity",
                line={"color": "#1f9d55", "width": 2},
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[_dt(int(row["timestamp_ms"])) for row in points],
                y=[float(Decimal(str(row.get("pnl", 0)))) for row in points],
                mode="lines",
                name="PnL",
                line={"color": "#7c3aed", "width": 2},
            )
        )
    fig.update_layout(height=260, margin={"l": 10, "r": 10, "t": 30, "b": 10}, template="plotly_white")
    return fig


def runner_counters_figure(rows: list[dict[str, Any]]) -> go.Figure:
    fig = go.Figure()
    points = [row for row in rows if row.get("timestamp_ms")]
    for name, color in [("orders", "#2563eb"), ("rejects", "#d64545"), ("api_errors", "#f59e0b")]:
        if points:
            fig.add_trace(
                go.Scatter(
                    x=[_dt(int(row["timestamp_ms"])) for row in points],
                    y=[int(row.get(name) or 0) for row in points],
                    mode="lines+markers",
                    name=name,
                    line={"color": color, "width": 2},
                )
            )
    fig.update_layout(height=220, margin={"l": 10, "r": 10, "t": 30, "b": 10}, template="plotly_white")
    return fig


def command_status_figure(commands: list[dict[str, Any]]) -> go.Figure:
    fig = go.Figure()
    counts: dict[str, int] = {}
    for command in commands:
        status = str(command.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    if counts:
        fig.add_trace(
            go.Bar(
                x=list(counts.keys()),
                y=list(counts.values()),
                marker={"color": ["#2563eb", "#1f9d55", "#d64545", "#6b7280"][: len(counts)]},
                name="Commands",
            )
        )
    fig.update_layout(height=220, margin={"l": 10, "r": 10, "t": 30, "b": 10}, template="plotly_white")
    return fig
