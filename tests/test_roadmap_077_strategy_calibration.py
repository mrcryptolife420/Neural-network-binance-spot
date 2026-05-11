from __future__ import annotations

import io
import json
import os
import tempfile
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.config import BotSettings
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.strategy_calibration import (
    build_strategy_dataset,
    calibrate_confidence,
    calibrate_strategy,
    paper_promotion_gate,
    rank_indicator_profiles,
    rank_symbols,
    run_backtest_calibration,
)
from binance_spot_bot.types import Candle, TradingMode


def settings(tmp: str) -> BotSettings:
    return BotSettings(
        app_env="local",
        trading_mode=TradingMode.TESTNET,
        binance_base_url="https://api.binance.com",
        binance_testnet_base_url="https://demo-api.binance.com",
        binance_api_key="",
        binance_api_secret="",
        live_trading_enabled=False,
        kill_switch=False,
        manual_live_approval="",
        max_daily_loss_quote=Decimal("50"),
        max_position_quote=Decimal("25"),
        max_trades_per_day=5,
        min_signal_confidence=0.1,
        max_spread_bps=Decimal("50"),
        data_dir=Path(tmp) / "data",
        audit_log_path=Path(tmp) / "data" / "audit" / "events.jsonl",
        exchange_profile=BINANCE_DEMO_SPOT_PROFILE,
        binance_demo_base_url="https://demo-api.binance.com",
    )


def candles(count: int = 150, start: Decimal = Decimal("100")) -> list[Candle]:
    rows = []
    for index in range(count):
        price = start + Decimal(index) * Decimal("0.2")
        rows.append(
            Candle(
                open_time_ms=1_700_000_000_000 + index * 60_000,
                open=price,
                high=price + Decimal("1"),
                low=price - Decimal("1"),
                close=price + Decimal("0.3"),
                volume=Decimal("10") + Decimal(index % 4),
                close_time_ms=1_700_000_059_999 + index * 60_000,
                quote_volume=Decimal("100000"),
                trade_count=30,
            )
        )
    return rows


def test_strategy_dataset_builder_uses_chronological_splits_and_no_lookahead() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        s = settings(tmp)
        result = calibrate_strategy(s.data_dir, {"BTCUSDT": candles(), "ETHUSDT": candles(start=Decimal("50"))})
        dataset = result.datasets[0]

        assert result.status == "ready"
        assert dataset.leakage_guard == "pass"
        assert dataset.train > dataset.validation > 0
        assert dataset.test > 0
        assert Path(dataset.feature_path).exists()
        assert Path(result.report_paths["markdown"]).exists()


def test_confidence_indicator_symbol_backtest_and_paper_gate_are_evidence_based() -> None:
    rows = {"BTCUSDT": candles(), "ETHUSDT": candles(start=Decimal("50"))}
    confidence = calibrate_confidence(rows)
    symbols = rank_symbols(rows)
    indicators = rank_indicator_profiles(rows)
    backtests = run_backtest_calibration(rows)
    gate = paper_promotion_gate(confidence, backtests)

    assert all(row["status"] == "ready" for row in confidence)
    assert symbols[0]["score"] >= symbols[-1]["score"]
    assert indicators[0]["score"] >= indicators[-1]["score"]
    assert all(row["status"] == "ready" for row in backtests)
    assert gate["status"] == "paper_approved"
    assert gate["scope"] == "paper_only"
    assert gate["live_trading_enabled"] is False


def test_strategy_dataset_can_be_built_individually() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        from binance_spot_bot.data import DataStore

        dataset = build_strategy_dataset(DataStore(settings(tmp).data_dir), "BTCUSDT", "1m", candles())

    assert dataset.dataset_id == "BTCUSDT_1m_strategy_calibration"
    assert dataset.features > 0
    assert dataset.labels > 0


def test_strategy_calibration_cli_exports_json() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        env = {"DATA_DIR": str(Path(tmp) / "data"), "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl")}
        buf = io.StringIO()
        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "strategy-calibrate", "--symbols", "BTCUSDT", "--json"]), redirect_stdout(buf):
            cli_main()
        payload = json.loads(buf.getvalue())

    assert payload["status"] == "ready"
    assert payload["promotion_gate"]["scope"] == "paper_only"
