from __future__ import annotations

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from binance_spot_bot.cache_manager import write_cache_manifest
from binance_spot_bot.chaos import simulate_failure
from binance_spot_bot.dashboard_profiler import DashboardProfiler
from binance_spot_bot.evidence import EvidenceVault
from binance_spot_bot.experiment_db import ExperimentDB
from binance_spot_bot.html_reports import export_html_report
from binance_spot_bot.notebook_export import export_notebook
from binance_spot_bot.portfolio import Portfolio
from binance_spot_bot.portfolio_paper_session import export_portfolio_report, run_portfolio_paper_session
from binance_spot_bot.portfolio_risk import PortfolioRiskEngine, PortfolioRiskLimits
from binance_spot_bot.readiness import score_readiness
from binance_spot_bot.scanner_history import ScannerHistory, ScannerRow, rank_watchlist
from binance_spot_bot.shadow import ShadowMode
from binance_spot_bot.testnet_endurance import TestnetEnduranceGuard
from binance_spot_bot.types import OrderSide, OrderType, TradeIntent


class ExperimentPortfolioReadinessTests(unittest.TestCase):
    def test_experiment_db_and_scanner_history_do_not_trade(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = ExperimentDB(Path(tmp) / "experiments.json")
            history = ScannerHistory(Path(tmp) / "scanner.jsonl", db)
            run = history.record_run([ScannerRow("BTCUSDT", 2.0, 1000.0, "BUY", 0.8)])
            rows = history.list_runs()
        self.assertFalse(run["orders_allowed"])
        self.assertEqual(rows[0]["rows"][0]["symbol"], "BTCUSDT")
        self.assertEqual(rank_watchlist([ScannerRow("A", 1, 1, "HOLD", 0.1)])[0].symbol, "A")

    def test_notebook_html_and_cache_exports_are_local_redacted_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "cache").mkdir()
            (root / "cache" / "item.json").write_text("{}", encoding="utf-8")
            nb = export_notebook("Report", {"api_secret": "abcdefghijklmnopqrstuvwxyz"}, root / "report.ipynb")
            html = export_html_report("Report", {"api_secret": "abcdefghijklmnopqrstuvwxyz"}, root / "report.html")
            manifest = write_cache_manifest(root / "cache", root / "cache-manifest.json")
            nb_payload = json.loads(nb.read_text(encoding="utf-8"))
            self.assertTrue(html.exists())
            self.assertTrue(manifest.exists())
            self.assertIn("[REDACTED]", json.dumps(nb_payload))
            profiler = DashboardProfiler()
            with profiler.measure("render"):
                _ = 1 + 1
            self.assertEqual(profiler.to_dict()["samples"][0]["name"], "render")

    def test_portfolio_and_risk_limits(self):
        portfolio = Portfolio()
        portfolio.set_balance("USDT", Decimal("1000"))
        portfolio.buy("BTCUSDT", "USDT", Decimal("100"), Decimal("100"), slippage_bps=Decimal("5"))
        self.assertGreater(portfolio.total_exposure({"BTCUSDT": Decimal("100")}), Decimal("0"))
        risk = PortfolioRiskEngine(PortfolioRiskLimits(Decimal("50"), 1, Decimal("10"), per_symbol_cooldown_ms=0))
        allowed, reason = risk.can_enter(portfolio, "ETHUSDT", {"BTCUSDT": Decimal("100"), "ETHUSDT": Decimal("10")})
        self.assertFalse(allowed)
        self.assertIn("exposure", reason)

    def test_portfolio_paper_session_and_testnet_guard(self):
        risk = PortfolioRiskEngine(PortfolioRiskLimits(Decimal("1000"), 3, Decimal("10"), per_symbol_cooldown_ms=0))
        result = run_portfolio_paper_session(["BTCUSDT", "ETHUSDT", "BNBUSDT"], Decimal("1000"), {"BTCUSDT": Decimal("100"), "ETHUSDT": Decimal("10"), "BNBUSDT": Decimal("1")}, risk)
        guard = TestnetEnduranceGuard(max_orders=1)
        self.assertEqual(result.status, "completed")
        self.assertFalse(guard.allow_order("https://api.binance.com")[0])
        self.assertTrue(guard.allow_order("https://testnet.binance.vision")[0])
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(export_portfolio_report(result, Path(tmp) / "portfolio.json").exists())
        guard.record_unresolved("abc")
        self.assertEqual(guard.cancel_open_orders(), ["abc"])

    def test_evidence_shadow_chaos_and_readiness(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = EvidenceVault(Path(tmp) / "evidence.jsonl")
            record = vault.add("check-all", {"status": "ok"})
            self.assertTrue(vault.verify(record))
            self.assertTrue(vault.export(Path(tmp) / "evidence.json").exists())
        shadow = ShadowMode()
        shadow.record_market_data({"symbol": "BTCUSDT"})
        shadow.record_intent(TradeIntent("BTCUSDT", OrderSide.BUY, Decimal("10"), OrderType.MARKET, Decimal("5")))
        with self.assertRaises(RuntimeError):
            shadow.place_order()
        self.assertEqual(simulate_failure("418").expected_action.value, "stop_runtime")
        readiness = score_readiness({"check-all", "paper-report", "secret-scan"})
        self.assertFalse(readiness.live_allowed)
        self.assertEqual(readiness.level, "R3")


if __name__ == "__main__":
    unittest.main()
