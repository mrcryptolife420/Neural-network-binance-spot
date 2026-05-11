from __future__ import annotations


OVERVIEW_CANDLESTICK = "overview.candlestick"
OVERVIEW_EQUITY = "overview.equity"
DEMO_PILOT_HEARTBEAT = "demo_pilot.runner.heartbeat"
DEMO_PILOT_COUNTERS = "demo_pilot.runner.counters"
DEMO_PILOT_EQUITY_PNL = "demo_pilot.runner.equity_pnl"
DEMO_PILOT_COMMAND_STATUS = "demo_pilot.runner.command_status"


def all_chart_keys() -> tuple[str, ...]:
    return (
        OVERVIEW_CANDLESTICK,
        OVERVIEW_EQUITY,
        DEMO_PILOT_HEARTBEAT,
        DEMO_PILOT_COUNTERS,
        DEMO_PILOT_EQUITY_PNL,
        DEMO_PILOT_COMMAND_STATUS,
    )
