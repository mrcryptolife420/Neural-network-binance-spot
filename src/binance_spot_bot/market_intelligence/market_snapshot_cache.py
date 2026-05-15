from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload


@dataclass(frozen=True)
class MarketSnapshotRecord:
    endpoint: str
    symbol: str
    payload: dict[str, Any]
    fetched_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    source: str = "fixture"
    live_trading_enabled: bool = False


def demo_market_snapshot(symbol: str) -> dict[str, Any]:
    seed = sum(ord(ch) for ch in symbol) % 100
    price = 100 + seed
    return {
        "symbol": symbol,
        "lastPrice": str(price),
        "bidPrice": str(price - 0.05),
        "askPrice": str(price + 0.05),
        "volume": str(1000 + seed),
        "quoteVolume": str((1000 + seed) * price),
        "priceChangePercent": str((seed % 10) - 5),
        "highPrice": str(price * 1.03),
        "lowPrice": str(price * 0.97),
        "avgPrice": str(price),
        "klines": [[idx * 60_000, str(price + idx * 0.1), str(price + idx * 0.2), str(price - idx * 0.1), str(price + idx * 0.05), "10", idx * 60_000 + 59_999] for idx in range(30)],
    }


class MarketSnapshotCache:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, endpoint: str, symbol: str, payload: dict[str, Any], *, source: str = "fixture") -> Path:
        record = MarketSnapshotRecord(endpoint=endpoint, symbol=symbol.upper(), payload=redact_payload(payload), source=source)
        path = self.root / endpoint / f"{symbol.upper()}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(redact_payload(asdict(record)), indent=2, default=str), encoding="utf-8")
        return path

    def load(self, endpoint: str, symbol: str, *, max_age_ms: int = 300_000) -> dict[str, Any]:
        path = self.root / endpoint / f"{symbol.upper()}.json"
        if not path.exists():
            return {"status": "missing", "symbol": symbol.upper(), "endpoint": endpoint, "live_trading_enabled": False}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"status": "failed", "symbol": symbol.upper(), "endpoint": endpoint, "warning": "corrupt cache", "live_trading_enabled": False}
        age_ms = int(time.time() * 1000) - int(payload.get("fetched_at_ms", 0))
        payload["age_ms"] = age_ms
        payload["status"] = "fresh" if age_ms <= max_age_ms else "stale"
        return redact_payload(payload)

    def seed_demo(self, symbols: list[str] | tuple[str, ...]) -> dict[str, Any]:
        paths = []
        for symbol in symbols:
            snapshot = demo_market_snapshot(symbol.upper())
            paths.append(str(self.write("ticker", symbol, snapshot)))
            paths.append(str(self.write("book_ticker", symbol, snapshot)))
            paths.append(str(self.write("klines", symbol, {"klines": snapshot["klines"]})))
        return {"status": "ok", "paths": paths, "live_trading_enabled": False}


def default_market_snapshot_cache(root: Path | str = ".") -> MarketSnapshotCache:
    return MarketSnapshotCache(Path(root) / "data" / "market-intelligence" / "snapshots")
