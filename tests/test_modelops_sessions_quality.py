import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.data_quality import check_candles
from binance_spot_bot.demo import DemoMarketReplay
from binance_spot_bot.evaluation import evaluate_rule_baseline, time_series_folds
from binance_spot_bot.features import build_feature_rows, build_label_rows
from binance_spot_bot.model_registry import ModelRegistry
from binance_spot_bot.session_store import SessionStore
from binance_spot_bot.signal_model import TinyNeuralSignalModel
from binance_spot_bot.types import Candle


class ModelOpsSessionsQualityTests(unittest.TestCase):
    def test_session_store_write_read_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SessionStore(Path(tmp))
            summary = store.start_session(mode="demo", symbol="BTCUSDT", interval="1m", model_version="m1")
            store.record_snapshot(summary.session_id, {"equity": "1000"})
            store.record_fill(summary.session_id, {"side": "BUY", "quantity": "1"})
            finished = store.finish_session(
                summary.session_id,
                pnl=Decimal("1"),
                max_drawdown=Decimal("0.5"),
                trades=1,
                blocks=2,
                status="completed",
            )
            self.assertEqual(finished.trades, 1)
            self.assertEqual(len(store.list_sessions()), 1)
            self.assertTrue(store.export_session_jsonl(summary.session_id).exists())
            self.assertTrue(store.export_fills_csv(summary.session_id).exists())

    def test_model_registry_register_and_load_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            candles = DemoMarketReplay(count=60).candles()
            features = build_feature_rows("BTCUSDT", candles, window=5)
            labels = build_label_rows(candles, window=5, horizon_bars=2)
            model = TinyNeuralSignalModel()
            model.fit(features, labels, epochs=2)
            registry = ModelRegistry(Path(tmp))
            metadata = registry.register(model, alias="candidate", dataset_id="demo", metrics={"rows": len(features)})
            loaded = registry.load_by_alias("candidate")
            self.assertIsNotNone(loaded)
            self.assertEqual(registry.get_by_alias("candidate").model_id, metadata.model_id)

    def test_evaluation_uses_chronological_gap(self):
        folds = time_series_folds(100, n_splits=3, test_size=10, gap=2)
        self.assertTrue(folds)
        for fold in folds:
            self.assertLess(fold.train_end, fold.test_start)
            self.assertGreaterEqual(fold.test_start - fold.train_end, 2)
        report = evaluate_rule_baseline("BTCUSDT", "1m", DemoMarketReplay(count=120).candles())
        self.assertFalse(report.shuffled)
        self.assertTrue(report.folds)

    def test_data_quality_warnings(self):
        candles = [
            Candle(0, Decimal("1"), Decimal("1"), Decimal("1"), Decimal("1"), Decimal("1"), 59_999),
            Candle(0, Decimal("1"), Decimal("1"), Decimal("1"), Decimal("1"), Decimal("1"), 59_999),
            Candle(180_000, Decimal("0"), Decimal("1"), Decimal("0"), Decimal("1"), Decimal("1"), 239_999),
        ]
        report = check_candles(candles, now_ms=500_000, spread_bps=Decimal("1000"), max_spread_bps=Decimal("30"))
        codes = {issue.code for issue in report.issues}
        self.assertIn("duplicate_timestamps", codes)
        self.assertIn("zero_or_negative_prices", codes)
        self.assertIn("extreme_spread", codes)

    def test_cli_smoke_new_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {
                "DATA_DIR": str(Path(tmp) / "data"),
                "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
            }
            for argv in [
                ["spot-bot", "register-demo-model", "--alias", "candidate"],
                ["spot-bot", "evaluate-model", "--symbol", "BTCUSDT", "--interval", "1m"],
                ["spot-bot", "data-quality", "--symbol", "BTCUSDT", "--interval", "1m"],
                ["spot-bot", "stream-paper", "--source", "demo", "--steps", "8"],
                ["spot-bot", "list-sessions"],
            ]:
                buf = io.StringIO()
                with patch.dict(os.environ, env, clear=True), patch("sys.argv", argv), redirect_stdout(buf):
                    cli_main()
                self.assertTrue(buf.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
