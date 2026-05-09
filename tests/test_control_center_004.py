import json
import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.config import BotSettings
from binance_spot_bot.connectivity import connectivity_report
from binance_spot_bot.credentials import CredentialManager, WindowsSecretStoreAdapter
from binance_spot_bot.exchange_profiles import (
    BINANCE_DEMO_SPOT_PROFILE,
    LOCAL_DEMO_PROFILE,
    selectable_profile_names,
)
from binance_spot_bot.launcher import dashboard_command, find_free_port
from binance_spot_bot.order_lifecycle import OrderLifecycleStore
from binance_spot_bot.redaction import fingerprint, redact_payload, redact_text
from binance_spot_bot.settings_store import DashboardSettings, DashboardSettingsStore
from binance_spot_bot.types import TradingMode
from binance_spot_bot.ui.state import SELECTABLE_MODES
from binance_spot_bot.user_data_stream import (
    BalanceUpdateEvent,
    ExecutionReportEvent,
    parse_user_data_message,
)


class FakeAdapter:
    def get_order_book(self, symbol, depth=5):
        return {"lastUpdateId": 123, "bids": [], "asks": []}

    def server_time(self):
        return 1_000

    def get_symbol_filters(self, symbol):
        from binance_spot_bot.types import SymbolFilters

        return SymbolFilters(
            symbol=symbol,
            status="TRADING",
            tick_size=Decimal("0.01"),
            step_size=Decimal("0.001"),
            min_qty=Decimal("0.001"),
            max_qty=Decimal("100"),
            min_notional=Decimal("5"),
        )

    def get_account_state(self):
        return {"canTrade": True, "accountType": "SPOT"}


class ControlCenter004Tests(unittest.TestCase):
    def test_profiles_and_ui_do_not_expose_live(self):
        self.assertIn(LOCAL_DEMO_PROFILE, selectable_profile_names())
        self.assertIn(BINANCE_DEMO_SPOT_PROFILE, selectable_profile_names())
        self.assertNotIn("live", selectable_profile_names())
        self.assertNotIn("live", SELECTABLE_MODES)

    def test_config_supports_binance_api_base_url_alias(self):
        env = {
            "TRADING_MODE": "testnet",
            "EXCHANGE_PROFILE": BINANCE_DEMO_SPOT_PROFILE,
            "BINANCE_API_BASE_URL": "https://demo-api.binance.com/api",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = BotSettings.from_env()
        self.assertEqual(settings.exchange_profile, BINANCE_DEMO_SPOT_PROFILE)
        self.assertEqual(settings.active_base_url, "https://demo-api.binance.com/api")

    def test_credential_manager_session_only_and_redacted(self):
        manager = CredentialManager()
        status = manager.set_session_credentials(BINANCE_DEMO_SPOT_PROFILE, "abcd1234efgh5678ijkl9012mnop3456", "secret-value-1234567890")
        self.assertTrue(status.has_api_key)
        self.assertIn("abcd", status.api_key_fingerprint)
        self.assertNotIn("efgh5678", status.api_key_fingerprint)
        safe = manager.apply_to_settings(BotSettings.from_env(), BINANCE_DEMO_SPOT_PROFILE)
        self.assertEqual(safe.trading_mode, TradingMode.TESTNET)
        manager.clear()
        self.assertFalse(manager.status().has_api_key)

    def test_redaction_masks_sensitive_values(self):
        text = (
            "BINANCE_API_SECRET="
            + "abcdefghijklmnopqrstuvwxyz123456"
            + " signature="
            + "abc12345678901234567890"
            + " listenKey="
            + "lk12345678901234567890"
        )
        redacted = redact_text(text)
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz", redacted)
        self.assertNotIn("abc1234567890", redacted)
        payload = redact_payload({"api_key": "abcd1234efgh5678ijkl9012mnop3456", "nested": {"signature": "sig123456789012345"}})
        self.assertEqual(payload["api_key"], "[REDACTED]")
        self.assertEqual(payload["nested"]["signature"], "[REDACTED]")

    def test_connectivity_report_with_fake_adapter(self):
        settings = BotSettings.from_env()
        settings = CredentialManager().apply_to_settings(settings, LOCAL_DEMO_PROFILE)
        report = connectivity_report(settings, "BTCUSDT", FakeAdapter())
        self.assertEqual(report["status"], "ok")
        self.assertFalse(report["live_trading_enabled"])

    def test_user_data_parsers_and_order_lifecycle(self):
        balance = parse_user_data_message({"e": "balanceUpdate", "E": 1, "a": "BTC", "d": "1.5", "T": 2})
        self.assertIsInstance(balance, BalanceUpdateEvent)
        report = parse_user_data_message(
            {
                "e": "executionReport",
                "E": 10,
                "s": "BTCUSDT",
                "c": "client-1",
                "S": "BUY",
                "o": "MARKET",
                "x": "TRADE",
                "X": "FILLED",
                "r": "NONE",
                "i": 99,
                "l": "0.1",
                "z": "0.1",
                "L": "100",
                "n": "0",
                "N": None,
                "T": 11,
            }
        )
        self.assertIsInstance(report, ExecutionReportEvent)
        store = OrderLifecycleStore()
        store.record_intent("client-1", "BTCUSDT", "BUY")
        lifecycle = store.apply_execution_report(report)
        self.assertEqual(lifecycle.status, "FILLED")
        self.assertFalse(lifecycle.needs_reconciliation)
        unknown = store.mark_submitted_unknown("client-2", "timeout")
        self.assertTrue(unknown.needs_reconciliation)

    def test_settings_store_never_writes_secrets_and_recovers_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = DashboardSettingsStore(Path(tmp))
            settings = DashboardSettings(selected_profile=BINANCE_DEMO_SPOT_PROFILE, symbol="ETHUSDT")
            path = store.save(settings)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertNotIn("api_key", payload)
            path.write_text("{not-json", encoding="utf-8")
            self.assertEqual(store.load().symbol, "BTCUSDT")

    def test_launcher_free_port_and_command_handle_spaced_path(self):
        port = find_free_port(8700)
        self.assertGreaterEqual(port, 8700)
        command = dashboard_command(Path("C:/Project With Spaces"), port)
        self.assertIn("streamlit", command)
        self.assertTrue(any("Project With Spaces" in part for part in command))

    def test_windows_secret_store_adapter_can_be_mocked(self):
        class Result:
            returncode = 0
            stdout = "Get-Secret"

        with patch("subprocess.run", return_value=Result()):
            self.assertTrue(WindowsSecretStoreAdapter().is_available())


if __name__ == "__main__":
    unittest.main()
