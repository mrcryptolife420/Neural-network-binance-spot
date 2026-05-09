from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .types import FeatureRow, Signal


@dataclass(frozen=True)
class SignalExplanation:
    signal: str
    confidence: float
    horizon: str
    model_version: str
    top_features: list[tuple[str, float]]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def explain_signal(signal: Signal, row: FeatureRow, top_n: int = 5) -> SignalExplanation:
    ranked = sorted(row.values.items(), key=lambda item: abs(float(item[1])), reverse=True)[:top_n]
    return SignalExplanation(
        signal=signal.signal.value,
        confidence=signal.confidence,
        horizon=signal.horizon,
        model_version=signal.model_version,
        top_features=[(key, float(value)) for key, value in ranked],
        metadata=signal.metadata,
    )
