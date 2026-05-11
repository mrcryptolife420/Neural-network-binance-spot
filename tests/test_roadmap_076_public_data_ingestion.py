from __future__ import annotations

import io
import json
import os
import tempfile
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.binance import BinanceSpotAdapter
from binance_spot_bot.binance_data_ingestion import (
    BinanceDataIngestionService,
    IngestionRequest,
    export_public_data_evidence,
)
from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.config import BotSettings
from binance_spot_bot.data import DataStore
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.indicator_warmup import multi_timeframe_indicator_context, warmup_indicators
from binance_spot_bot.public_data_quality import order_book_liquidity, ticker_context, trade_flow_features
from binance_spot_bot.public_ws_ingestion import build_public_ws_plan
from binance_spot_bot.types import TradingMode


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


def raw_klines(count: int = 130) -> list[list[str | int]]:
    rows = []
    for index in range(count):
        price = Decimal("100") + Decimal(index) / Decimal("10")
        rows.append(
            [
                1_700_000_000_000 + index * 60_000,
                str(price),
                str(price + Decimal("1")),
                str(price - Decimal("1")),
                str(price + Decimal("0.5")),
                "10",
                1_700_000_059_999 + index * 60_000,
                "1000",
                25,
            ]
        )
    return rows


class RecordingPublicAdapter(BinanceSpotAdapter):
    def __init__(self, settings: BotSettings):
        super().__init__(settings)
        self.calls: list[dict[str, object]] = []

    def _request(self, method, path, params=None, signed=False):
        self.calls.append({"method": method, "path": path, "params": params or {}, "signed": signed})
        if path == "/api/v3/exchangeInfo":
            return {"symbols": [{"symbol": "BTCUSDT", "status": "TRADING", "filters": []}]}
        if path in {"/api/v3/klines", "/api/v3/uiKlines"}:
            return raw_klines(130)
        if path == "/api/v3/depth":
            return {"bids": [["100", "2"], ["99", "2"]], "asks": [["101", "2"], ["102", "2"]]}
        if path == "/api/v3/ticker/24hr":
            return {"symbol": "BTCUSDT", "priceChangePercent": "1.5", "quoteVolume": "200000", "count": 1000}
        if path == "/api/v3/ticker":
            return {"symbol": "BTCUSDT", "priceChangePercent": "0.5"}
        if path == "/api/v3/avgPrice":
            return {"mins": 5, "price": "100"}
        if path == "/api/v3/trades":
            return [{"price": "100", "qty": "0.2"}, {"price": "101", "qty": "0.4"}]
        if path == "/api/v3/aggTrades":
            return [{"p": "100", "q": "0.2"}]
        if path == "/api/v3/ticker/bookTicker":
            return {"bidPrice": "100", "askPrice": "101"}
        raise AssertionError(path)


class FailingAdapter(RecordingPublicAdapter):
    def _request(self, method, path, params=None, signed=False):
        raise RuntimeError("offline")


def test_public_binance_client_methods_are_unsigned() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        adapter = RecordingPublicAdapter(settings(tmp))
        adapter.get_24hr_ticker("BTCUSDT")
        adapter.get_rolling_ticker("BTCUSDT", "1h")
        adapter.get_avg_price("BTCUSDT")
        adapter.get_recent_trades("BTCUSDT")
        adapter.get_agg_trades("BTCUSDT")
        adapter.get_book_ticker("BTCUSDT")
        adapter.get_ui_klines("BTCUSDT", "1m")

    assert adapter.calls
    assert all(call["signed"] is False for call in adapter.calls)
    assert not any(call["path"] in {"/api/v3/account", "/api/v3/order", "/api/v3/openOrders"} for call in adapter.calls)


def test_ingestion_warms_multiple_symbols_saves_manifest_and_cache_fallback() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        s = settings(tmp)
        service = BinanceDataIngestionService(s, adapter=RecordingPublicAdapter(s))
        result = service.ingest(IngestionRequest(["BTCUSDT", "ETHUSDT"], intervals=["1m", "5m"], candle_limit=130))
        manifest_path = Path(result.manifests[0])
        verify = DataStore(s.data_dir).verify_data_manifest(manifest_path)
        cached = BinanceDataIngestionService(s, adapter=FailingAdapter(s)).ingest(
            IngestionRequest(["BTCUSDT"], intervals=["1m"], candle_limit=130, offline_ok=True)
        )
        assert manifest_path.exists()

    assert result.status == "ok"
    assert len(result.bundles) == 2
    assert result.bundles[0].quality["status"] in {"healthy", "warning"}
    assert verify["status"] == "ok"
    assert cached.status == "ok"
    assert cached.bundles[0].source == "cache-fallback"


def test_indicator_warmup_quality_liquidity_market_context_and_ws_plan() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        s = settings(tmp)
        service = BinanceDataIngestionService(s, adapter=RecordingPublicAdapter(s))
        payload = warmup_indicators(s, ["BTCUSDT"], candle_limit=130, service=service)
        bundle = service.ingest(IngestionRequest(["BTCUSDT"], intervals=["1m", "5m"], candle_limit=130)).bundles[0]
        mtf = multi_timeframe_indicator_context(bundle)
        evidence = export_public_data_evidence(s)
        assert evidence.exists()
    liquidity = order_book_liquidity({"bids": [["100", "20"]], "asks": [["100.01", "20"]]})
    market = ticker_context({"priceChangePercent": "1.2", "quoteVolume": "100000", "count": 100})
    flow = trade_flow_features([{"price": "100", "qty": "0.1"}])
    ws = build_public_ws_plan(["BTCUSDT"], enabled=False)

    assert payload["status"] == "ready"
    assert payload["rows"][0]["candles_loaded"] == 130
    assert mtf["timeframe_agreement_score"] >= 0
    assert liquidity["score"] > 0
    assert market["volume_score"] > 0
    assert flow["recent_trade_count"] == 1
    assert ws["credentials_required"] is False


def test_public_data_cli_commands_with_fake_service() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        env = {"DATA_DIR": str(Path(tmp) / "data"), "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl")}
        buf = io.StringIO()
        with (
            patch.dict(os.environ, env, clear=False),
            patch("binance_spot_bot.binance_data_ingestion.BinanceSpotAdapter", RecordingPublicAdapter),
            patch("sys.argv", ["spot-bot", "fetch-public-data", "--symbols", "BTCUSDT", "--intervals", "1m", "--limit", "130", "--json"]),
            redirect_stdout(buf),
        ):
            cli_main()
        payload = json.loads(buf.getvalue())

    assert payload["status"] == "ok"
    assert payload["live_trading_enabled"] is False
