from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from binance_spot_bot.multi_symbol import (
    allocation_plan,
    choose_active_symbols,
    next_multi_action,
    normalize_symbol,
    parse_symbol_list,
    risk_limit_rows,
    summarize_multi_rows,
    validate_demo_symbols,
    write_multi_symbol_evidence,
)
from binance_spot_bot.ui.charts import multi_symbol_overview_figure


def test_normalize_symbol_adds_usdt_for_short_base_assets() -> None:
    assert normalize_symbol("eth") == "ETHUSDT"
    assert normalize_symbol("sol-usdt") == "SOLUSDT"
    assert normalize_symbol("BTCUSDT") == "BTCUSDT"


def test_parse_symbol_list_deduplicates_and_caps() -> None:
    symbols = parse_symbol_list("btc, ETHUSDT eth sol xrp ada", max_symbols=3)

    assert symbols == ["BTCUSDT", "ETHUSDT", "SOLUSDT"]


def test_choose_active_symbols_combines_selected_and_custom_with_limit() -> None:
    symbols = choose_active_symbols(["BTCUSDT", "ETHUSDT"], "SOL, XRPUSDT, ADA", max_active=4)

    assert symbols == ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]


def test_validate_demo_symbols_reports_empty_and_non_usdt_warning() -> None:
    assert validate_demo_symbols([], max_active=3)["status"] == "fail"

    payload = validate_demo_symbols(["BTCBUSD"], max_active=3)

    assert payload["status"] == "warn"
    assert payload["warnings"][0]["name"] == "symbols.quote_asset"


def test_allocation_plan_warns_when_order_size_exceeds_symbol_budget() -> None:
    rows = allocation_plan(
        ["BTCUSDT", "ETHUSDT"],
        total_quote_budget=Decimal("20"),
        default_quote_size=Decimal("15"),
        max_position_quote=Decimal("100"),
    )

    assert rows[0]["quote_budget"] == "10.00"
    assert rows[0]["status"] == "warn"


def test_risk_rows_and_summary_are_demo_safe() -> None:
    risk_rows = risk_limit_rows(
        ["BTCUSDT"],
        max_open_orders_per_symbol=2,
        max_trades=5,
        max_position_quote=Decimal("25"),
        max_daily_loss=Decimal("10"),
        max_spread=Decimal("30"),
        min_conf=0.2,
    )
    summary = summarize_multi_rows(
        [
            {"symbol": "BTCUSDT", "status": "running", "fills": 2, "open_orders": 1, "equity": "1001.5"},
            {"symbol": "ETHUSDT", "status": "stopped", "fills": 1, "open_orders": 0, "equity": "999.5"},
        ]
    )

    assert risk_rows[0]["live_trading_enabled"] is False
    assert summary["active_bots"] == 1
    assert summary["total_fills"] == 3
    assert summary["total_equity"] == "2001.0"


def test_next_multi_action_guides_operator() -> None:
    assert next_multi_action(has_keys=False, connection_status="not-tested", armed=False, validation_status="ok", running=False) == "Enter demo keys"
    assert next_multi_action(has_keys=True, connection_status="ok", armed=True, validation_status="fail", running=False) == "Fix selected symbols"
    assert next_multi_action(has_keys=True, connection_status="ok", armed=True, validation_status="ok", running=False) == "Start selected symbols"


def test_write_multi_symbol_evidence(tmp_path: Path) -> None:
    payload = write_multi_symbol_evidence(
        tmp_path,
        symbols=["BTCUSDT"],
        rows=[{"symbol": "BTCUSDT", "status": "running", "fills": 0, "open_orders": 0, "equity": "1000"}],
        validation={"status": "ok", "live_trading_enabled": False},
        allocation=[{"symbol": "BTCUSDT", "quote_budget": "100.00"}],
        summary={"active_bots": 1, "live_trading_enabled": False},
    )

    assert payload["live_trading_enabled"] is False
    assert Path(payload["path"]).exists()


def test_multi_symbol_overview_figure_contains_order_and_equity_traces() -> None:
    fig = multi_symbol_overview_figure(
        [
            {"symbol": "BTCUSDT", "fills": 2, "open_orders": 1, "equity": "1001"},
            {"symbol": "ETHUSDT", "fills": 1, "open_orders": 0, "equity": "999"},
        ]
    )

    assert [trace.name for trace in fig.data] == ["Fills", "Open orders", "Equity"]
    assert fig.layout.height == 280
