from __future__ import annotations

from decimal import Decimal
from typing import Any

from .signal_model import TinyNeuralSignalModel
from .types import FeatureRow, LabelRow


def train_tiny_model(features: list[FeatureRow], labels: list[LabelRow], *, hidden_size: int = 6, seed: int = 7, epochs: int = 20, learning_rate: float = 0.03) -> TinyNeuralSignalModel:
    model = TinyNeuralSignalModel(hidden_size=hidden_size, seed=seed)
    model.fit(features, labels, epochs=epochs, lr=learning_rate)
    return model


def train_model(rows: int) -> dict[str, Any]:
    if rows <= 0:
        return {"status": "blocked", "reason": "rows_required", "live_trading_enabled": False}
    return {"status": "ok", "rows": rows, "model_type": "tiny_neural_signal", "live_trading_enabled": False}


def synthetic_training_rows(rows: int) -> tuple[list[FeatureRow], list[LabelRow]]:
    features: list[FeatureRow] = []
    labels: list[LabelRow] = []
    for index in range(max(1, rows)):
        ts = index * 60_000
        ret = ((index % 5) - 2) / 1000
        features.append(
            FeatureRow(
                "BTCUSDT",
                ts,
                {
                    "ret_1": ret,
                    "ret_window": ret * 2,
                    "rolling_volatility": abs(ret) / 2,
                    "volume_zscore": float(index % 3),
                },
                Decimal("100") + Decimal(index),
            )
        )
        labels.append(LabelRow(ts, 3, ret, 1 if ret > 0 else 0))
    return features, labels
