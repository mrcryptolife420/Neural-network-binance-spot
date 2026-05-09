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
    fig.update_layout(
        height=520,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        xaxis_rangeslider_visible=False,
        legend_orientation="h",
        template="plotly_white",
    )
    return fig


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

