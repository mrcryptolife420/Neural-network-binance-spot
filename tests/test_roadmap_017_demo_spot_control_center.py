from __future__ import annotations

import tempfile
import time
import unittest
from decimal import Decimal
from pathlib import Path

from binance_spot_bot.audit import AuditLog
from binance_spot_bot.binance import BinanceAPIError, BinanceSpotAdapter
from binance_spot_bot.config import BotSettings
from binance_spot_bot.connectivity import demo_spot_connection_state
from binance_spot_bot.demo_spot import DEMO_SPOT_BASE_URL, evaluate_demo_trading_gate, normalize_base_url
from binance_spot_bot.execution import ExecutionEngine
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.risk import RiskEngine, RiskLimits
from binance_spot_bot.types import AccountState, MarketState, Signal, SignalSide, SymbolFilters, TradingMode


class FakeDemoOrderAdapter:
    def __init__(self) -> None:
        self.tested = False
        self.placed = False

    def test_order(self, order):
        self.tested = True
        return {}

    def place_order(self, order):
        self.placed = True
        return {"symbol": order.symbol, "status": "FILLED", "orderId": 123, "executedQty": str(order.quantity)}


class FakeConnectivityAdapter:
    def get_order_book(self, symbol, depth=5):
        return {"lastUpdateId": 1}

    def server_time(self):
        return int(time.time() * 1000)

    def get_symbol_filters(self, symbol):
        return filters()

    def get_account_state(self):
        return {"canTrade": True, "accountType": "SPOT", "balances": []}


def demo_settings(tmp: str, base_url: str = DEMO_SPOT_BASE_URL) -> BotSettings:
    return BotSettings(
        app_env="local",
        trading_mode=TradingMode.TESTNET,
        binance_base_url="https://api.binance.com",
        binance_testnet_base_url=base_url,
        binance_api_key="demo-key",
        binance_api_secret="demo-secret",
        live_trading_enabled=False,
        kill_switch=False,
        manual_live_approval="",
        max_daily_loss_quote=Decimal("50"),
        max_position_quote=Decimal("25"),
        max_trades_per_day=5,
        min_signal_confidence=0.1,
        max_spread_bps=Decimal("50"),
        data_dir=Path(tmp) / "data",
        audit_log_path=Path(tmp) / "data" / "audit" / "events.jsonl",
        exchange_profile=BINANCE_DEMO_SPOT_PROFILE,
        binance_demo_base_url=base_url,
    )


def filters() -> SymbolFilters:
    return SymbolFilters("BTCUSDT", "TRADING", Decimal("0.01"), Decimal("0.00001"), Decimal("0.00001"), Decimal("100"), Decimal("5"))


def allowed_decision():
    limits = RiskLimits(Decimal("50"), Decimal("25"), 5, 0.1, Decimal("50"), default_quote_size=Decimal("10"))
    return RiskEngine(limits, kill_switch=False).decide(
        Signal(SignalSide.BUY, 0.9, "3 bars", "test"),
        AccountState(quote_balance=Decimal("100")),
        MarketState("BTCUSDT", Decimal("100"), Decimal("99.9"), Decimal("100.1"), 1, 1),
    )


class Roadmap017DemoSpotControlCenterTests(unittest.TestCase):
    def test_demo_gate_requires_profile_base_url_credentials_and_arm(self):
        blocked = evaluate_demo_trading_gate(
            profile="local-demo",
            base_url=DEMO_SPOT_BASE_URL,
            has_credentials=True,
            connection_ok=True,
            armed=True,
            live_trading_enabled=False,
            kill_switch=False,
            risk_allowed=True,
            filters_loaded=True,
            max_orders_ok=True,
        )
        allowed = evaluate_demo_trading_gate(
            profile=BINANCE_DEMO_SPOT_PROFILE,
            base_url=DEMO_SPOT_BASE_URL + "/api",
            has_credentials=True,
            connection_ok=True,
            armed=True,
            live_trading_enabled=False,
            kill_switch=False,
            risk_allowed=True,
            filters_loaded=True,
            max_orders_ok=True,
        )
        self.assertFalse(blocked.allowed)
        self.assertTrue(allowed.allowed)
        self.assertEqual(normalize_base_url(DEMO_SPOT_BASE_URL + "/api"), DEMO_SPOT_BASE_URL)

    def test_adapter_blocks_non_demo_order_base_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            adapter = BinanceSpotAdapter(demo_settings(tmp, base_url="https://api.binance.com"))
            with self.assertRaises(BinanceAPIError):
                adapter.open_orders("BTCUSDT")

    def test_execution_demo_order_requires_arm_and_calls_test_before_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = demo_settings(tmp)
            fake = FakeDemoOrderAdapter()
            unarmed = ExecutionEngine(settings, AuditLog(settings.audit_log_path), fake, demo_trading_armed=False)
            blocked = unarmed.execute(allowed_decision(), MarketState("BTCUSDT", Decimal("100")), filters())
            armed = ExecutionEngine(settings, AuditLog(settings.audit_log_path), fake, demo_trading_armed=True)
            result = armed.execute(allowed_decision(), MarketState("BTCUSDT", Decimal("100")), filters())
        self.assertEqual(blocked.status, "BLOCKED")
        self.assertEqual(result.status, "FILLED")
        self.assertTrue(fake.tested)
        self.assertTrue(fake.placed)

    def test_demo_connection_state_uses_redacted_connectivity_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = demo_spot_connection_state(
                demo_settings(tmp),
                "BTCUSDT",
                armed=True,
                api_key_fingerprint="demo...7890",
                adapter=FakeConnectivityAdapter(),
            )
        self.assertTrue(state["connected"])
        self.assertTrue(state["authenticated"])
        self.assertTrue(state["trading_permission_ok"])
        self.assertNotIn("demo-secret", str(state))


if __name__ == "__main__":
    unittest.main()
