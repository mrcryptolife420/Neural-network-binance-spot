from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from binance_spot_bot.demo import DemoMarketReplay
from binance_spot_bot.indicators import (
    INDICATOR_PROFILES,
    allocation_hints,
    choose_indicator_profile,
    detect_regime,
    indicator_snapshot,
    indicator_summary,
    write_indicator_evidence,
)


def test_indicator_snapshot_contains_adaptive_fields() -> None:
    candles = DemoMarketReplay(scenario="uptrend", count=80).candles()

    row = indicator_snapshot("BTCUSDT", candles, "auto")

    assert row["profile"] in INDICATOR_PROFILES
    assert row["bias"] in {"BUY", "SELL", "HOLD"}
    assert row["live_trading_enabled"] is False
    assert "reason" in row


def test_regime_and_profile_are_deterministic() -> None:
    candles = DemoMarketReplay(scenario="volatile", count=80).candles()
    regime = detect_regime(candles)

    assert regime["regime"] in {"high_volatility", "uptrend", "downtrend", "range"}
    assert choose_indicator_profile(candles, "trend") == "trend"
    assert choose_indicator_profile(candles, "auto") in INDICATOR_PROFILES


def test_indicator_summary_and_allocation_hints() -> None:
    rows = [
        {"symbol": "BTCUSDT", "bias": "BUY", "confidence": 0.7, "regime": "uptrend"},
        {"symbol": "ETHUSDT", "bias": "HOLD", "confidence": 0.1, "regime": "range"},
    ]

    summary = indicator_summary(rows)
    hints = allocation_hints(rows, Decimal("100"))

    assert summary["bias_counts"]["BUY"] == 1
    assert summary["live_trading_enabled"] is False
    assert hints[0]["symbol"] == "BTCUSDT"
    assert hints[0]["note"] == "informational only"


def test_indicator_evidence_export(tmp_path: Path) -> None:
    rows = [indicator_snapshot("BTCUSDT", DemoMarketReplay(count=80).candles(), "auto")]

    payload = write_indicator_evidence(tmp_path, rows, "auto", True)

    assert payload["live_trading_enabled"] is False
    assert Path(payload["path"]).exists()
