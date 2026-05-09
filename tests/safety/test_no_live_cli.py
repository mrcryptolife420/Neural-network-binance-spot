import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.manual_demo_trading import ManualDemoTradeRequest, execute_manual_demo_trade
from binance_spot_bot.types import OrderSide, SymbolFilters


class NoLiveCliTests(unittest.TestCase):
    def test_control_center_dry_run_keeps_live_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {
                "DATA_DIR": str(Path(tmp) / "data"),
                "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
            }
            argv = ["spot-bot", "control-center", "--dry-run", "--no-browser"]
            buf = io.StringIO()
            with patch.dict(os.environ, env, clear=True), patch("sys.argv", argv), redirect_stdout(buf):
                cli_main()
        payload = json.loads(buf.getvalue())
        self.assertFalse(payload["live_trading_enabled"])
        self.assertTrue(payload["kill_switch"])

    def test_manual_demo_trade_uses_no_signed_exchange_adapter(self):
        filters = SymbolFilters("BTCUSDT", "TRADING", Decimal("0.01"), Decimal("0.00001"), Decimal("0.00001"), Decimal("100"), Decimal("5"))
        request = ManualDemoTradeRequest(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            quote_size=Decimal("25"),
            price=Decimal("100"),
            quote_balance=Decimal("1000"),
            confirmed_demo_only=True,
        )
        result = execute_manual_demo_trade(request, filters)
        self.assertEqual(result.status, "PAPER_FILLED")
        self.assertEqual(result.fill["origin"], "manual_demo")
        self.assertNotIn("order_id", result.fill)


if __name__ == "__main__":
    unittest.main()
