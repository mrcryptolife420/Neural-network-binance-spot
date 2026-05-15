from __future__ import annotations

from binance_spot_bot.dashboard_smoke_v2 import dashboard_smoke_v2
from binance_spot_bot.ui.chart_registry import all_chart_keys
from binance_spot_bot.ui.components import MAX_DEBUG_CHARS, MAX_TABLE_ROWS, limit_debug_payload, limit_table_rows
from binance_spot_bot.ui.page_registry import PAGES, dashboard_page_contract, page_by_key, validate_page_registry
from binance_spot_bot.ui.state import SELECTABLE_MODES


def test_dashboard_page_registry_has_lazy_no_live_budget_contract() -> None:
    validate_page_registry()
    contract = dashboard_page_contract()

    assert contract["status"] == "ok"
    assert contract["lazy_sections"] is True
    assert "live" not in SELECTABLE_MODES
    assert all(page.live_trading_enabled is False for page in PAGES)
    assert all(page.performance_budget_ms > 0 for page in PAGES)
    assert {"overview", "demo_spot_trading", "demo_pilot", "performance"}.issubset(set(contract["smoke_pages"]))


def test_dedicated_page_modules_are_lazy_importable_without_live_trading() -> None:
    for key in ["overview", "demo_spot_trading", "demo_pilot", "performance"]:
        renderer = page_by_key(key).load_renderer()
        payload = renderer()
        assert payload["page"] == key
        assert payload["live_trading_enabled"] is False


def test_dashboard_component_payload_limits_redact_and_cap() -> None:
    rows, truncated = limit_table_rows([{"row": i} for i in range(MAX_TABLE_ROWS + 10)])
    debug = limit_debug_payload({"api_secret": "abcdefghijklmnopqrstuvwxyz", "blob": "x" * (MAX_DEBUG_CHARS + 500)})

    assert len(rows) == MAX_TABLE_ROWS
    assert truncated is True
    assert debug["truncated"] is True
    assert "[REDACTED]" in str(debug["payload"])


def test_dashboard_smoke_v2_validates_keys_lazy_sections_and_no_live() -> None:
    payload = dashboard_smoke_v2()
    chart_keys = all_chart_keys()

    assert len(chart_keys) == len(set(chart_keys))
    assert payload["status"] == "ok"
    assert payload["payload"]["stable_keys"] is True
    assert payload["payload"]["lazy_sections"] is True
    assert payload["payload"]["payload_limits"]["table_limit_applied"] is True
    assert payload["payload"]["payload_limits"]["debug_limit_applied"] is True
    assert payload["payload"]["no_live_mode"] is True
    assert payload["live_trading_enabled"] is False
