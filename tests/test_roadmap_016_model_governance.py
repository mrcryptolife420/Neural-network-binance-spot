from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from binance_spot_bot.dataset_governance import (
    DatasetManifest,
    build_dataset_manifest,
    feature_schema_from_rows,
    leakage_guard,
    validate_feature_schema,
)
from binance_spot_bot.dataset_model_wizard import DatasetWizardConfig, save_dataset_manifest_from_rows
from binance_spot_bot.demo import DemoMarketReplay
from binance_spot_bot.evaluation import WalkForwardConfig, evaluate_walk_forward, walk_forward_folds
from binance_spot_bot.experiment_db import ExperimentDB
from binance_spot_bot.features import build_feature_rows, build_label_rows
from binance_spot_bot.model_registry import ModelRegistry
from binance_spot_bot.signal_model import TinyNeuralSignalModel


class Roadmap016ModelGovernanceTests(unittest.TestCase):
    def test_dataset_manifest_schema_hash_and_roundtrip(self):
        candles = DemoMarketReplay(count=90).candles()
        features = build_feature_rows("BTCUSDT", candles, window=5)
        labels = build_label_rows(candles, window=5, horizon_bars=2)
        manifest = build_dataset_manifest(
            dataset_id="demo-dataset",
            source="demo",
            symbol="BTCUSDT",
            interval="1m",
            candles=candles,
            features=features,
            labels=labels,
            train_rows=features[:40],
            validation_rows=features[42:55],
            test_rows=features[57:70],
            lookback_window=5,
            label_horizon=2,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = manifest.save(Path(tmp) / "manifest.json")
            loaded = DatasetManifest.load(path)
        self.assertEqual(loaded.checksum, manifest.checksum)
        self.assertEqual(loaded.feature_schema_hash, feature_schema_from_rows(features, lookback_window=5).schema_hash)
        validate_feature_schema(features, loaded.feature_schema_hash, lookback_window=5)

    def test_leakage_guard_blocks_bad_splits(self):
        candles = DemoMarketReplay(count=60).candles()
        features = build_feature_rows("BTCUSDT", candles, window=5)
        labels = build_label_rows(candles, window=5, horizon_bars=2)
        report = leakage_guard(
            features,
            labels,
            train_rows=features[:20],
            validation_rows=features[19:30],
            test_rows=features[32:40],
            label_horizon=2,
        )
        codes = {issue.code for issue in report.issues}
        self.assertFalse(report.passed)
        self.assertIn("train_validation_overlap", codes)

    def test_walk_forward_evaluation_reports_costs_and_leakage(self):
        candles = DemoMarketReplay(count=160).candles()
        config = WalkForwardConfig(n_splits=3, gap=2)
        folds = walk_forward_folds(120, config)
        report = evaluate_walk_forward("BTCUSDT", "1m", candles, config=config)
        payload = report_to_jsonable(report)
        self.assertTrue(folds)
        self.assertEqual(payload["mode"], "walk_forward")
        self.assertEqual(payload["leakage"]["status"], "pass")
        self.assertIn("fee_bps", payload["costs"])
        self.assertIn("baseline", payload["folds"][0])
        self.assertIn("candidate", payload["folds"][0])

    def test_model_registry_promotion_gates_and_model_card(self):
        candles = DemoMarketReplay(count=120).candles()
        features = build_feature_rows("BTCUSDT", candles, window=5)
        labels = build_label_rows(candles, window=5, horizon_bars=2)
        model = TinyNeuralSignalModel()
        model.fit(features, labels, epochs=2)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "manifest.json"
            report_path = root / "walkforward.json"
            manifest_path.write_text("{}", encoding="utf-8")
            report_path.write_text("{}", encoding="utf-8")
            registry = ModelRegistry(root / "models")
            metadata = registry.register(
                model,
                alias="candidate",
                dataset_id="demo",
                feature_schema_hash=feature_schema_from_rows(features, lookback_window=5).schema_hash,
                manifest_path=str(manifest_path),
                walkforward_report_path=str(report_path),
                metrics={
                    "leakage_pass": True,
                    "candidate_beats_baseline": True,
                    "trade_count": 3,
                    "min_trade_count": 1,
                    "max_drawdown_quote": 1,
                    "max_allowed_drawdown_quote": 10,
                },
            )
            self.assertTrue(Path(metadata.model_card_path).exists())
            blocked = registry.promote_to_champion(metadata.model_id, operator_confirmed=False)
            allowed = registry.promote_to_champion(metadata.model_id, operator_confirmed=True)
        self.assertFalse(blocked.allowed)
        self.assertIn("operator_confirmed", blocked.reasons)
        self.assertTrue(allowed.allowed)

    def test_wizard_manifest_and_experiment_filter(self):
        candles = DemoMarketReplay(count=90).candles()
        features = build_feature_rows("BTCUSDT", candles, window=5)
        labels = build_label_rows(candles, window=5, horizon_bars=2)
        config = DatasetWizardConfig(
            "BTCUSDT",
            "1m",
            features[0].timestamp_ms,
            features[35].timestamp_ms,
            features[50].timestamp_ms,
            features[70].timestamp_ms,
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = save_dataset_manifest_from_rows(
                dataset_id="wizard-demo",
                source="demo",
                config=config,
                candles=candles,
                features=features,
                labels=labels,
                lookback_window=5,
                label_horizon=2,
                path=root / "manifest.json",
            )
            db = ExperimentDB(root / "experiments.json")
            db.add_dataset_manifest(str(root / "manifest.json"), {"dataset_id": manifest.dataset_id, "status": "pass"})
            rows = db.filter(kind="dataset_manifest", dataset_id="wizard-demo", status="pass")
        self.assertEqual(len(rows), 1)


def report_to_jsonable(report):
    return json.loads(json.dumps(report.__dict__, default=str))


if __name__ == "__main__":
    unittest.main()
