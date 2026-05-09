from __future__ import annotations

import math
import random
from dataclasses import dataclass
from decimal import Decimal

from .types import Candle


@dataclass(frozen=True)
class DemoMarketReplay:
    symbol: str = "BTCUSDT"
    interval_ms: int = 60_000
    scenario: str = "sideways"
    seed: int = 7
    count: int = 240

    def candles(self) -> list[Candle]:
        rng = random.Random(self.seed)
        price = Decimal("100.00")
        rows: list[Candle] = []
        for i in range(self.count):
            drift = self._drift(i)
            noise = Decimal(str(round(rng.uniform(-0.18, 0.18), 4)))
            open_price = price
            close = max(Decimal("1"), price + drift + noise)
            swing = Decimal("0.20") + abs(noise) + Decimal(str(round(rng.random() * 0.15, 4)))
            high = max(open_price, close) + swing
            low = min(open_price, close) - swing
            volume = Decimal("12") + Decimal(str(round(abs(float(noise)) * 35 + rng.random() * 8, 4)))
            rows.append(
                Candle(
                    open_time_ms=i * self.interval_ms,
                    open=open_price.quantize(Decimal("0.0001")),
                    high=high.quantize(Decimal("0.0001")),
                    low=low.quantize(Decimal("0.0001")),
                    close=close.quantize(Decimal("0.0001")),
                    volume=volume.quantize(Decimal("0.0001")),
                    close_time_ms=i * self.interval_ms + self.interval_ms - 1,
                    quote_volume=(volume * close).quantize(Decimal("0.0001")),
                    trade_count=20 + int(volume),
                )
            )
            price = close
        return rows

    def _drift(self, index: int) -> Decimal:
        wave = Decimal(str(round(math.sin(index / 9) * 0.08, 4)))
        if self.scenario == "uptrend":
            return Decimal("0.045") + wave
        if self.scenario == "downtrend":
            return Decimal("-0.045") + wave
        if self.scenario == "volatile":
            return Decimal(str(round(math.sin(index / 3) * 0.22, 4)))
        return wave

