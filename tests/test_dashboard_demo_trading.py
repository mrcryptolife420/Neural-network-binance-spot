from __future__ import annotations

import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.config import BotSettings
from binance_spot_bot.dashboard_state import BotEngineStatus, bot_status_from_runtime
from binance_spot_bot.manual_demo_trading import ManualDemoTradeRequest, execute_manual_demo_trade, preview_manual_demo_trade
from binance_spot_bot.spot_preview import load_spot_symbol_preview
from binance_spot_bot.types import OrderSide, SymbolFilters
from binance_spot_bot.ui.wizard import option_for, wizard_options


class FakePublicSpotAdapter:
    def get_symbol_filters(self, symbol: str) -> SymbolFilters:
        return SymbolFilters(symbol, "TRADING", Decimal("0.01"), Decimal("0.001"), Decimal("0.001"), Decimal("100"), Decimal("5"))

    def get_order_book(self, symbol: str, depth: int = 5) -> dict[str, list[list[str]]]:
        return {"bids": [["99.90", "1"]], "asks": [["100.10", "1"]]}

    def get_klines(self, symbol: str, interval: str, limit: int = 60) -> list[list[object]]:
        return [
            [1, "99", "101", "98", "100", "1", 2, "100", 1],
            [3, "100", "102", "99", "101", "1", 4, "101", 1],
        ]


class DashboardDemoTradingTests(unittest.TestCase):
    def filters(self) -> SymbolFilters:
        return SymbolFilters("BTCUSDT", "TRADING", Decimal("0.01"), Decimal("0.00001"), Decimal("0.00001"), Decimal("100"), Decimal("5"))

    def settings(self) -> BotSettings:
        with tempfile.TemporaryDirectory() as tmp:
            env = {
                "DATA_DIR": str(Path(tmp) / "data"),
                "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
            }
            with patch.dict(os.environ, env, clear=True):
                return BotSettings.from_env()

    def test_dashboard_state_maps_runtime_status(self):
        self.assertEqual(bot_status_from_runtime("running"), BotEngineStatus.RUNNING)
        self.assertEqual(bot_status_from_runtime("unexpected"), BotEngineStatus.ERROR)

    def test_wizard_options_exclude_live_mode(self):
        modes = {item["mode"] for item in wizard_options()}
        self.assertNotIn("live", modes)
        self.assertFalse(option_for("local-demo").requires_keys)

    def test_spot_preview_uses_public_adapter_only(self):
        preview = load_spot_symbol_preview(self.settings(), "BTCUSDT", adapter=FakePublicSpotAdapter())
        self.assertEqual(preview.source, "public-rest")
        self.assertEqual(preview.last_price, Decimal("101"))
        self.assertEqual(preview.filters.min_notional, Decimal("5"))

    def test_manual_demo_buy_creates_local_paper_fill(self):
        request = ManualDemoTradeRequest(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            quote_size=Decimal("25"),
            price=Decimal("100"),
            quote_balance=Decimal("1000"),
            confirmed_demo_only=True,
        )
        result = execute_manual_demo_trade(request, self.filters())
        self.assertEqual(result.status, "PAPER_FILLED")
        self.assertEqual(result.fill["origin"], "manual_demo")

    def test_manual_demo_blocks_unconfirmed_or_underfunded_sell(self):
        unconfirmed = ManualDemoTradeRequest(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            quote_size=Decimal("25"),
            price=Decimal("100"),
            quote_balance=Decimal("1000"),
        )
        self.assertFalse(preview_manual_demo_trade(unconfirmed, self.filters()).allowed)
        sell = ManualDemoTradeRequest(
            symbol="BTCUSDT",
            side=OrderSide.SELL,
            quote_size=Decimal("25"),
            price=Decimal("100"),
            quote_balance=Decimal("1000"),
            base_balance=Decimal("0"),
            confirmed_demo_only=True,
        )
        self.assertEqual(execute_manual_demo_trade(sell, self.filters()).status, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
