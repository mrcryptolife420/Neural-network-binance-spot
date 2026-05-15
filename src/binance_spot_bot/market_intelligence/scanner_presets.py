from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .public_endpoint_policy import NO_LIVE_STATEMENT


@dataclass(frozen=True)
class ScannerPreset:
    preset_id: str
    symbols: tuple[str, ...]
    quote_asset: str = "USDT"
    ranking_dimension: str = "highest_quote_volume"
    max_symbols: int = 50
    no_live_statement: str = NO_LIVE_STATEMENT
    live_trading_enabled: bool = False


PRESETS = (
    ScannerPreset("majors_overview", ("BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT")),
    ScannerPreset("high_volume_usdt", ("BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"), ranking_dimension="highest_quote_volume"),
    ScannerPreset("low_spread_liquidity", ("BTCUSDT", "ETHUSDT", "BNBUSDT"), ranking_dimension="lowest_spread"),
    ScannerPreset("volatile_watch", ("SOLUSDT", "XRPUSDT", "ETHUSDT"), ranking_dimension="highest_volatility"),
    ScannerPreset("data_quality_watch", ("BTCUSDT", "ETHUSDT"), ranking_dimension="freshest_data"),
    ScannerPreset("paper_strategy_candidates", ("BTCUSDT", "ETHUSDT", "BNBUSDT"), ranking_dimension="liquidity_proxy"),
)


def scanner_presets_payload() -> dict[str, Any]:
    return redact_payload({"status": "ok", "presets": [asdict(item) for item in PRESETS], "live_trading_enabled": False})


def get_scanner_preset(preset_id: str) -> ScannerPreset:
    for preset in PRESETS:
        if preset.preset_id == preset_id:
            return preset
    raise ValueError(f"unknown scanner preset: {preset_id}")
