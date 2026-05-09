import os
import unittest
from decimal import Decimal
from unittest.mock import patch

from binance_spot_bot.config import BotSettings, ConfigError
from binance_spot_bot.types import TradingMode


class ConfigTests(unittest.TestCase):
    def test_default_config_is_disabled_and_kill_switch_on(self):
        with patch.dict(os.environ, {}, clear=True):
            settings = BotSettings.from_env()
        self.assertEqual(settings.trading_mode, TradingMode.DISABLED)
        self.assertTrue(settings.kill_switch)

    def test_live_mode_is_fail_closed(self):
        env = {
            "APP_ENV": "local",
            "TRADING_MODE": "live",
            "LIVE_TRADING_ENABLED": "false",
            "KILL_SWITCH": "true",
            "MAX_DAILY_LOSS_QUOTE": "0",
            "MAX_POSITION_QUOTE": "0",
            "MAX_TRADES_PER_DAY": "0",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = BotSettings.from_env()
        with self.assertRaises(ConfigError):
            settings.validate_live_readiness()

    def test_live_mode_requires_manual_phrase(self):
        env = {
            "APP_ENV": "live",
            "TRADING_MODE": "live",
            "LIVE_TRADING_ENABLED": "true",
            "KILL_SWITCH": "false",
            "MANUAL_LIVE_APPROVAL": "wrong",
            "MAX_DAILY_LOSS_QUOTE": "10",
            "MAX_POSITION_QUOTE": "10",
            "MAX_TRADES_PER_DAY": "1",
            "BINANCE_API_KEY": "key",
            "BINANCE_API_SECRET": "secret",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = BotSettings.from_env()
        with self.assertRaises(ConfigError):
            settings.validate_live_readiness()

    def test_paper_limits_parse(self):
        env = {
            "TRADING_MODE": "paper",
            "KILL_SWITCH": "false",
            "MAX_DAILY_LOSS_QUOTE": "50.5",
            "MAX_POSITION_QUOTE": "25",
            "MAX_TRADES_PER_DAY": "3",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = BotSettings.from_env()
        self.assertEqual(settings.max_daily_loss_quote, Decimal("50.5"))
        self.assertEqual(settings.trading_mode, TradingMode.PAPER)


if __name__ == "__main__":
    unittest.main()

