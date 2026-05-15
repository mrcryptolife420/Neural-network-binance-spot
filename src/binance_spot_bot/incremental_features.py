from __future__ import annotations

from typing import Any

from .features import build_feature_rows
from .types import Candle, FeatureRow


class IncrementalFeatureBuilder:
    def __init__(self, symbol: str, window: int = 20) -> None:
        self.symbol = symbol
        self.window = window
        self.candles: list[Candle] = []
        self.features: list[FeatureRow] = []

    def update(self, candles: list[Candle]) -> dict[str, Any]:
        seen = {candle.open_time_ms for candle in self.candles}
        self.candles.extend(candle for candle in candles if candle.open_time_ms not in seen)
        self.candles.sort(key=lambda item: item.open_time_ms)
        rebuilt = build_feature_rows(self.symbol, self.candles, self.window)
        known = {row.timestamp_ms for row in self.features}
        new_rows = [row for row in rebuilt if row.timestamp_ms not in known]
        self.features.extend(new_rows)
        return {"status": "ok", "new_rows": len(new_rows), "total_rows": len(self.features), "live_trading_enabled": False}

    def latest(self) -> FeatureRow | None:
        return self.features[-1] if self.features else None
