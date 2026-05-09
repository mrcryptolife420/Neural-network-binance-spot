from __future__ import annotations

import csv
import json
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

from .types import Candle, FeatureRow, LabelRow


def _json_default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    return str(value)


class DataStore:
    def __init__(self, root: Path):
        self.root = root
        self.raw_dir = root / "raw"
        self.processed_dir = root / "processed"
        self.features_dir = root / "features"
        self.models_dir = root / "models"
        for path in [self.raw_dir, self.processed_dir, self.features_dir, self.models_dir]:
            path.mkdir(parents=True, exist_ok=True)

    def save_raw_json(self, name: str, payload: Any) -> Path:
        path = self.raw_dir / f"{name}.json"
        path.write_text(json.dumps(payload, default=_json_default, indent=2), encoding="utf-8")
        return path

    def save_candles_csv(self, symbol: str, interval: str, candles: Iterable[Candle]) -> Path:
        path = self.processed_dir / f"{symbol}_{interval}_candles.csv"
        rows = list(candles)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()) if rows else [])
            if rows:
                writer.writeheader()
                for row in rows:
                    writer.writerow({k: str(v) for k, v in asdict(row).items()})
        return path

    def load_candles_csv(self, symbol: str, interval: str) -> list[Candle]:
        path = self.processed_dir / f"{symbol}_{interval}_candles.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            return [
                Candle(
                    open_time_ms=int(row["open_time_ms"]),
                    open=Decimal(row["open"]),
                    high=Decimal(row["high"]),
                    low=Decimal(row["low"]),
                    close=Decimal(row["close"]),
                    volume=Decimal(row["volume"]),
                    close_time_ms=int(row["close_time_ms"]),
                    quote_volume=Decimal(row["quote_volume"]),
                    trade_count=int(row["trade_count"]),
                )
                for row in csv.DictReader(handle)
            ]

    def save_feature_rows(self, dataset_id: str, rows: Iterable[FeatureRow]) -> Path:
        path = self.features_dir / f"{dataset_id}_features.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(asdict(row), default=_json_default, sort_keys=True) + "\n")
        return path

    def save_label_rows(self, dataset_id: str, rows: Iterable[LabelRow]) -> Path:
        path = self.features_dir / f"{dataset_id}_labels.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(asdict(row), default=_json_default, sort_keys=True) + "\n")
        return path


def parse_binance_klines(raw_klines: list[list[Any]]) -> list[Candle]:
    candles = [
        Candle(
            open_time_ms=int(row[0]),
            open=Decimal(str(row[1])),
            high=Decimal(str(row[2])),
            low=Decimal(str(row[3])),
            close=Decimal(str(row[4])),
            volume=Decimal(str(row[5])),
            close_time_ms=int(row[6]),
            quote_volume=Decimal(str(row[7])),
            trade_count=int(row[8]),
        )
        for row in raw_klines
    ]
    validate_candles(candles)
    return candles


def validate_candles(candles: list[Candle]) -> None:
    previous = -1
    for candle in candles:
        if candle.open_time_ms <= previous:
            raise ValueError("Candles must be strictly chronological")
        if candle.low > candle.high:
            raise ValueError("Candle low cannot exceed high")
        previous = candle.open_time_ms

