import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.config import BotSettings
from binance_spot_bot.demo import DemoMarketReplay
from binance_spot_bot.runtime import BotRuntime, RuntimeOptions
from binance_spot_bot.ui.state import SELECTABLE_MODES


def settings_for_tmp(tmp: str) -> BotSettings:
    return BotSettings(
        app_env="local",
        trading_mode="disabled",
        binance_base_url="https://api.binance.com",
        binance_testnet_base_url="https://testnet.binance.vision",
        binance_api_key="",
        binance_api_secret="",
        live_trading_enabled=False,
        kill_switch=True,
        manual_live_approval="",
        max_daily_loss_quote=Decimal("0"),
        max_position_quote=Decimal("0"),
        max_trades_per_day=0,
        min_signal_confidence=0.15,
        max_spread_bps=Decimal("30"),
        data_dir=Path(tmp) / "data",
        audit_log_path=Path(tmp) / "data" / "audit" / "events.jsonl",
    )


class RuntimeDashboardTests(unittest.TestCase):
    def test_demo_replay_is_deterministic(self):
        first = DemoMarketReplay(seed=11, scenario="volatile", count=10).candles()
        second = DemoMarketReplay(seed=11, scenario="volatile", count=10).candles()
        self.assertEqual(first, second)

    def test_ui_modes_do_not_include_live(self):
        self.assertIn("demo", SELECTABLE_MODES)
        self.assertIn("paper", SELECTABLE_MODES)
        self.assertNotIn("live", SELECTABLE_MODES)

    def test_runtime_runs_demo_steps_without_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = BotRuntime(
                settings_for_tmp(tmp),
                RuntimeOptions(mode="demo", symbol="BTCUSDT", fetch_limit=90),
            )
            snapshot = runtime.run_steps(50)
        self.assertEqual(snapshot.mode, "demo")
        self.assertGreater(len(snapshot.candles), 0)
        self.assertIsNotNone(snapshot.current_candle)
        self.assertGreater(len(snapshot.audit_tail), 0)

    def test_cli_run_local_outputs_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {
                "DATA_DIR": str(Path(tmp) / "data"),
                "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
            }
            argv = [
                "spot-bot",
                "run-local",
                "--mode",
                "demo",
                "--symbol",
                "BTCUSDT",
                "--steps",
                "20",
            ]
            buf = io.StringIO()
            with patch.dict(os.environ, env, clear=True), patch("sys.argv", argv), redirect_stdout(buf):
                cli_main()
        self.assertIn('"mode": "demo"', buf.getvalue())
        self.assertIn('"symbol": "BTCUSDT"', buf.getvalue())


if __name__ == "__main__":
    unittest.main()
