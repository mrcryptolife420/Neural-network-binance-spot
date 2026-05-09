from __future__ import annotations

import json
import os
import tempfile
import unittest
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.alerts import AlertManager, AlertSeverity, WatchdogAction
from binance_spot_bot.config import BotSettings
from binance_spot_bot.paper_accounting import PaperAccount
from binance_spot_bot.preflight import run_preflight
from binance_spot_bot.session_report import export_session_report
from binance_spot_bot.session_store import SessionStore


class PreflightReportsAccountingTests(unittest.TestCase):
    def settings(self, tmp: str) -> BotSettings:
        env = {
            "DATA_DIR": str(Path(tmp) / "data"),
            "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
        }
        with patch.dict(os.environ, env, clear=True):
            return BotSettings.from_env()

    def test_preflight_ok_without_credentials_for_local_demo(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_preflight(self.settings(tmp), Path(tmp), include_security_scan=False)
        self.assertEqual(report.status, "ok")
        self.assertIn("live_disabled", {check.name for check in report.checks})

    def test_preflight_blocks_live_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = replace(self.settings(tmp), live_trading_enabled=True)
            report = run_preflight(settings, Path(tmp), include_security_scan=False)
        self.assertEqual(report.status, "blocked")

    def test_alert_manager_maps_severity_to_actions(self):
        alerts = AlertManager()
        alerts.emit("spread", AlertSeverity.ERROR, "spread too wide")
        critical = alerts.emit("runtime", AlertSeverity.CRITICAL, "runtime unsafe")
        self.assertTrue(alerts.should_block_trading())
        self.assertTrue(alerts.should_stop_runtime())
        self.assertEqual(critical.action, WatchdogAction.STOP_RUNTIME)

    def test_paper_accounting_buy_sell_fee_and_pnl(self):
        account = PaperAccount(quote_balance=Decimal("1000"), fee_bps=Decimal("10"))
        buy = account.buy("BTCUSDT", Decimal("1"), Decimal("100"))
        sell = account.sell("BTCUSDT", Decimal("1"), Decimal("110"))
        self.assertEqual(buy.side.value, "BUY")
        self.assertEqual(sell.realized_pnl, Decimal("9.89"))
        self.assertEqual(account.base_balance, Decimal("0"))

    def test_session_report_exports_redacted_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SessionStore(Path(tmp) / "sessions")
            session = store.start_session(
                mode="demo",
                symbol="BTCUSDT",
                interval="1m",
                model_version="demo",
                metadata={"api_secret": "not-written"},
            )
            store.record_snapshot(session.session_id, {"timestamp_ms": 1, "equity": "1000"})
            store.record_fill(session.session_id, {"symbol": "BTCUSDT", "side": "BUY"})
            paths = export_session_report(store, session.session_id)
            summary = json.loads(Path(paths["summary_json"]).read_text(encoding="utf-8"))
        self.assertEqual(summary["metadata"]["api_secret"], "[REDACTED]")
        self.assertTrue(paths["summary_md"].endswith("summary.md"))


if __name__ == "__main__":
    unittest.main()
