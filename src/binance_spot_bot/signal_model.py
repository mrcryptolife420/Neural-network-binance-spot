from __future__ import annotations

import json
import math
import random
from pathlib import Path

from .types import FeatureRow, LabelRow, Signal, SignalSide


class RuleBasedSignalModel:
    model_version = "rule-baseline-0.1"

    def predict(self, row: FeatureRow) -> Signal:
        ret = row.values.get("ret_window", 0.0)
        vol = row.values.get("rolling_volatility", 0.0)
        if ret > max(0.002, vol):
            return Signal(SignalSide.BUY, min(0.75, 0.55 + abs(ret) * 20), "3 bars", self.model_version)
        if ret < -max(0.002, vol):
            return Signal(SignalSide.SELL, min(0.75, 0.55 + abs(ret) * 20), "3 bars", self.model_version)
        return Signal(SignalSide.HOLD, 0.5, "3 bars", self.model_version)


class TinyNeuralSignalModel:
    """Small pure-Python MLP for deterministic local validation.

    This is intentionally compact. It proves the NN signal boundary without forcing
    heavyweight research dependencies into the safe scaffold.
    """

    def __init__(self, feature_names: list[str] | None = None, hidden_size: int = 6, seed: int = 7):
        self.feature_names = feature_names or []
        self.hidden_size = hidden_size
        self.model_version = "tiny-mlp-0.1"
        self._rng = random.Random(seed)
        self.w1: list[list[float]] = []
        self.b1: list[float] = []
        self.w2: list[float] = []
        self.b2 = 0.0

    def fit(self, features: list[FeatureRow], labels: list[LabelRow], epochs: int = 50, lr: float = 0.05) -> None:
        if not features or not labels:
            raise ValueError("features and labels are required")
        label_by_ts = {label.timestamp_ms: label.label for label in labels}
        rows = [(row, label_by_ts[row.timestamp_ms]) for row in features if row.timestamp_ms in label_by_ts]
        if not rows:
            raise ValueError("features and labels have no matching timestamps")
        self.feature_names = self.feature_names or sorted(rows[0][0].values.keys())
        if not self.w1:
            self._init_weights(len(self.feature_names))
        for _ in range(epochs):
            for row, target in rows:
                x = self._vector(row)
                hidden_raw = [
                    sum(x[i] * self.w1[h][i] for i in range(len(x))) + self.b1[h]
                    for h in range(self.hidden_size)
                ]
                hidden = [math.tanh(value) for value in hidden_raw]
                logit = sum(hidden[h] * self.w2[h] for h in range(self.hidden_size)) + self.b2
                pred = 1 / (1 + math.exp(-max(-30, min(30, logit))))
                error = pred - target
                for h in range(self.hidden_size):
                    grad_w2 = error * hidden[h]
                    self.w2[h] -= lr * grad_w2
                self.b2 -= lr * error
                for h in range(self.hidden_size):
                    grad_hidden = error * self.w2[h] * (1 - hidden[h] ** 2)
                    for i in range(len(x)):
                        self.w1[h][i] -= lr * grad_hidden * x[i]
                    self.b1[h] -= lr * grad_hidden

    def predict(self, row: FeatureRow) -> Signal:
        if not self.w1:
            return Signal(SignalSide.HOLD, 0.0, "untrained", self.model_version)
        x = self._vector(row)
        hidden = [
            math.tanh(sum(x[i] * self.w1[h][i] for i in range(len(x))) + self.b1[h])
            for h in range(self.hidden_size)
        ]
        logit = sum(hidden[h] * self.w2[h] for h in range(self.hidden_size)) + self.b2
        prob_up = 1 / (1 + math.exp(-max(-30, min(30, logit))))
        confidence = abs(prob_up - 0.5) * 2
        if confidence < 0.2:
            side = SignalSide.HOLD
        else:
            side = SignalSide.BUY if prob_up > 0.5 else SignalSide.SELL
        return Signal(side, confidence, "3 bars", self.model_version, {"prob_up": prob_up})

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "feature_names": self.feature_names,
            "hidden_size": self.hidden_size,
            "model_version": self.model_version,
            "w1": self.w1,
            "b1": self.b1,
            "w2": self.w2,
            "b2": self.b2,
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "TinyNeuralSignalModel":
        payload = json.loads(path.read_text(encoding="utf-8"))
        model = cls(payload["feature_names"], payload["hidden_size"])
        model.model_version = payload["model_version"]
        model.w1 = payload["w1"]
        model.b1 = payload["b1"]
        model.w2 = payload["w2"]
        model.b2 = payload["b2"]
        return model

    def _init_weights(self, input_size: int) -> None:
        self.w1 = [
            [self._rng.uniform(-0.1, 0.1) for _ in range(input_size)]
            for _ in range(self.hidden_size)
        ]
        self.b1 = [0.0 for _ in range(self.hidden_size)]
        self.w2 = [self._rng.uniform(-0.1, 0.1) for _ in range(self.hidden_size)]
        self.b2 = 0.0

    def _vector(self, row: FeatureRow) -> list[float]:
        return [float(row.values.get(name, 0.0)) for name in self.feature_names]

