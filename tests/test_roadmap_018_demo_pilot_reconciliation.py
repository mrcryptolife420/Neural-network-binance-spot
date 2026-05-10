from __future__ import annotations

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.config import BotSettings
from binance_spot_bot.demo_pilot import (
    DemoAccountSync,
    DemoOrderReconciler,
    DemoPilotCounters,
    pilot_config,
    should_pause_pilot,
)
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.order_lifecycle import OrderLifecycleStore
from binance_spot_bot.runtime import BotRuntime, RuntimeOptions
from binance_spot_bot.session_store import SessionStore
from binance_spot_bot.types import TradingMode


class FakePilotAdapter:
    def __init__(self, open_orders=None):
        self.open = list(open_orders or [])
        self.cancelled: list[int] = []
        self.queries: list[str] = []

    def open_orders(self, symbol):
        return list(self.open)

    def query_order(self, symbol, order_id=None, client_order_id=None):
        self.queries.append(client_order_id or str(order_id))
        return {
            "symbol": symbol,
            "side": "BUY",
            "status": "FILLED",
            "orderId": order_id or 10,
            "clientOrderId": client_order_id or "known-1",
            "executedQty": "0.1",
            "price": "100",
        }

    def cancel_order(self, symbol, order_id):
        self.cancelled.append(order_id)
        return {"symbol": symbol, "orderId": order_id, "status": "CANCELED"}

    def get_account_state(self):
        return {
            "canTrade": True,
            "accountType": "SPOT",
            "balances": [
                {"asset": "BTC", "free": "0.1", "locked": "0"},
                {"asset": "USDT", "free": "0", "locked": "0"},
            ],
        }

    def test_order(self, order):
        return {}

    def place_order(self, order):
        return {"symbol": order.symbol, "status": "NEW", "orderId": 10, "clientOrderId": order.client_order_id}


def demo_settings(tmp: str) -> BotSettings:
    return BotSettings(
        app_env="local",
        trading_mode=TradingMode.TESTNET,
        binance_base_url="https://api.binance.com",
        binance_testnet_base_url="https://demo-api.binance.com",
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
        binance_demo_base_url="https://demo-api.binance.com",
    )


class Roadmap018DemoPilotReconciliationTests(unittest.TestCase):
    def test_pilot_presets_and_pause_limits(self):
        config = pilot_config("smoke")
        paused, reason = should_pause_pilot(config, DemoPilotCounters(orders=config.max_demo_orders))
        self.assertEqual(config.pilot_name, "smoke")
        self.assertTrue(paused)
        self.assertIn("orders", reason)

    def test_reconciler_updates_known_and_detects_orphan_orders(self):
        store = OrderLifecycleStore()
        known = store.record_intent("known-1", "BTCUSDT", "BUY")
        known.order_id = 10
        adapter = FakePilotAdapter(
            [{"symbol": "BTCUSDT", "side": "BUY", "status": "NEW", "orderId": 99, "clientOrderId": "orphan-1"}]
        )
        result = DemoOrderReconciler(adapter, store).reconcile("BTCUSDT")
        self.assertEqual(result.status, "needs_operator_action")
        self.assertEqual(result.orphan_orders, 1)
        self.assertEqual(store.orders["known-1"].status, "FILLED")
        self.assertEqual(store.orders["orphan-1"].status, "ORPHAN_OPEN")

    def test_account_sync_filters_zero_balances(self):
        snapshot = DemoAccountSync(FakePilotAdapter()).sync()
        self.assertEqual(snapshot.status, "ok")
        self.assertEqual(snapshot.balances[0]["asset"], "BTC")
        self.assertEqual(len(snapshot.balances), 1)

    def test_runtime_clean_start_blocks_orphan_open_orders(self):
        adapter = FakePilotAdapter(
            [{"symbol": "BTCUSDT", "side": "BUY", "status": "NEW", "orderId": 99, "clientOrderId": "orphan-1"}]
        )
        with tempfile.TemporaryDirectory() as tmp, patch("binance_spot_bot.runtime.BinanceSpotAdapter", return_value=adapter):
            runtime = BotRuntime(demo_settings(tmp), RuntimeOptions(mode="demo", demo_trading_armed=True, source="demo"))
            snapshot = runtime.step()
        self.assertEqual(snapshot.status, "stopped")
        self.assertTrue(snapshot.resume_required)
        self.assertEqual(snapshot.reconciliation["status"], "needs_operator_action")

    def test_cancel_on_stop_records_cancel_and_report_metadata(self):
        adapter = FakePilotAdapter(
            [{"symbol": "BTCUSDT", "side": "BUY", "status": "NEW", "orderId": 99, "clientOrderId": "known-1"}]
        )
        with tempfile.TemporaryDirectory() as tmp, patch("binance_spot_bot.runtime.BinanceSpotAdapter", return_value=adapter):
            runtime = BotRuntime(demo_settings(tmp), RuntimeOptions(mode="demo", demo_trading_armed=True, source="demo"))
            runtime.demo_pilot_config = pilot_config("smoke")
            runtime.demo_pilot_config = runtime.demo_pilot_config.__class__(**{**runtime.demo_pilot_config.to_dict(), "require_clean_start": False})
            runtime.stop()
            summary = SessionStore(runtime.settings.data_dir / "sessions").load_summary(runtime.session.session_id)
            report = json.loads(Path(runtime.report_paths["summary_json"]).read_text(encoding="utf-8"))
            pilot_report = json.loads(Path(runtime.report_paths["demo_pilot_json"]).read_text(encoding="utf-8"))
        self.assertEqual(adapter.cancelled, [99])
        self.assertIn("demo_pilot", summary.metadata)
        self.assertIn("reconciliation", report["metadata"])
        self.assertIn("cancel_on_stop_status", pilot_report)


if __name__ == "__main__":
    unittest.main()
