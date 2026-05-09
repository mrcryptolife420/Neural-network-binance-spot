import unittest
from decimal import Decimal

from binance_spot_bot.backtest import BacktestEngine
from binance_spot_bot.data import parse_binance_klines
from binance_spot_bot.features import build_feature_rows, build_label_rows, chronological_split
from binance_spot_bot.risk import RiskEngine, RiskLimits
from binance_spot_bot.signal_model import RuleBasedSignalModel, TinyNeuralSignalModel


def demo_klines(count=50):
    rows = []
    price = Decimal("100")
    for i in range(count):
        open_price = price
        close = price + Decimal((i % 7) - 3) / Decimal("10")
        high = max(open_price, close) + Decimal("0.2")
        low = min(open_price, close) - Decimal("0.2")
        rows.append(
            [
                i * 60_000,
                str(open_price),
                str(high),
                str(low),
                str(close),
                "10",
                i * 60_000 + 59_999,
                "1000",
                10,
                "5",
                "500",
                "0",
            ]
        )
        price = close
    return rows


class FeatureModelBacktestTests(unittest.TestCase):
    def test_features_are_chronological_and_split(self):
        candles = parse_binance_klines(demo_klines())
        rows = build_feature_rows("BTCUSDT", candles, window=5)
        train, validation, test = chronological_split(rows)
        self.assertGreater(len(train), len(validation))
        self.assertGreater(len(test), 0)
        self.assertEqual([r.timestamp_ms for r in rows], sorted(r.timestamp_ms for r in rows))

    def test_tiny_neural_model_trains_and_predicts_schema(self):
        candles = parse_binance_klines(demo_klines())
        features = build_feature_rows("BTCUSDT", candles, window=5)
        labels = build_label_rows(candles, window=5, horizon_bars=2)
        model = TinyNeuralSignalModel()
        model.fit(features, labels, epochs=2)
        signal = model.predict(features[-1])
        self.assertIn(signal.signal.value, {"BUY", "SELL", "HOLD"})
        self.assertGreaterEqual(signal.confidence, 0)
        self.assertLessEqual(signal.confidence, 1)

    def test_backtest_runs_with_fees_and_slippage(self):
        candles = parse_binance_klines(demo_klines())
        features = build_feature_rows("BTCUSDT", candles, window=5)
        limits = RiskLimits(
            max_daily_loss_quote=Decimal("50"),
            max_position_quote=Decimal("20"),
            max_trades_per_day=10,
            min_signal_confidence=0.1,
            max_spread_bps=Decimal("50"),
        )
        result = BacktestEngine(RiskEngine(limits, kill_switch=False)).run(
            features, RuleBasedSignalModel()
        )
        self.assertGreaterEqual(result.trades + result.blocked, len(features))


if __name__ == "__main__":
    unittest.main()

