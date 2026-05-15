from __future__ import annotations

import json
from decimal import Decimal

from binance_spot_bot.data_pipeline_evidence import data_pipeline_lineage, write_data_pipeline_evidence
from binance_spot_bot.data_quality_v2 import data_quality_v2
from binance_spot_bot.data_store_v2 import DataStoreRoot
from binance_spot_bot.feature_store_contracts import contract_from_features, validate_feature_contract
from binance_spot_bot.incremental_features import IncrementalFeatureBuilder
from binance_spot_bot.indicator_compute import compute_indicator
from binance_spot_bot.types import Candle


def _candles(count: int = 30) -> list[Candle]:
    rows: list[Candle] = []
    for index in range(count):
        close = Decimal("100") + Decimal(index)
        rows.append(
            Candle(
                open_time_ms=index * 60_000,
                open=close - Decimal("1"),
                high=close + Decimal("2"),
                low=close - Decimal("2"),
                close=close,
                volume=Decimal("10") + Decimal(index),
                close_time_ms=index * 60_000 + 59_999,
                quote_volume=Decimal("1000"),
                trade_count=10 + index,
            )
        )
    return rows


def test_data_store_v2_writes_manifest_hashes_and_blocks_path_traversal(tmp_path) -> None:
    store = DataStoreRoot(tmp_path / "data")
    artifact = store.write_json("raw/BTCUSDT.json", {"api_secret": "abcdefghijklmnopqrstuvwxyz", "rows": [1]})
    manifest_path = store.write_manifest("dataset-1", [artifact])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert artifact.sha256
    assert manifest["artifacts"][0]["artifact_type"] == "json"
    assert "[REDACTED]" in (tmp_path / "data" / "raw" / "BTCUSDT.json").read_text(encoding="utf-8")
    assert manifest["live_trading_enabled"] is False
    try:
        store.write_json("../escape.json", {})
    except ValueError as exc:
        assert "outside root" in str(exc)
    else:
        raise AssertionError("path traversal must be blocked")


def test_indicator_registry_quality_and_incremental_feature_contract() -> None:
    candles = _candles()
    builder = IncrementalFeatureBuilder("BTCUSDT", window=5)
    first = builder.update(candles[:20])
    second = builder.update(candles[20:])
    contract = contract_from_features("dataset-1", builder.features, lookback_window=5)
    validation = validate_feature_contract(builder.features, contract)
    quality = data_quality_v2([{"timestamp_ms": candle.close_time_ms} for candle in candles])

    assert first["new_rows"] > 0
    assert second["new_rows"] > 0
    assert builder.latest() is not None
    assert validation["status"] == "ok"
    assert compute_indicator([1.0, 2.0, 3.0], "momentum")["value"] == 2.0
    assert compute_indicator([1.0], "unknown")["status"] == "blocked"
    assert quality["status"] == "ok"


def test_data_pipeline_lineage_evidence_is_redacted_and_no_live(tmp_path) -> None:
    path = write_data_pipeline_evidence(
        tmp_path / "evidence" / "data-pipeline.json",
        "dataset-1",
        [{"timestamp_ms": 1, "api_key": "abcdefghijklmnopqrstuvwxyz"}],
        {"raw": "raw.json", "features": "features.jsonl", "model": "model.json"},
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    lineage = data_pipeline_lineage("dataset-1", {"raw": "raw.json", "features": "features.jsonl"})

    assert payload["live_trading_enabled"] is False
    assert payload["quality"]["live_trading_enabled"] is False
    assert lineage["lineage"][0]["stage"] == "raw"
    assert "[REDACTED]" in path.read_text(encoding="utf-8")
