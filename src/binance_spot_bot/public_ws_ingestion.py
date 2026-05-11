from __future__ import annotations

from dataclasses import dataclass


PUBLIC_WS_STREAMS = ("kline", "miniTicker", "bookTicker", "depth", "aggTrade")


@dataclass(frozen=True)
class PublicWebSocketPlan:
    symbols: list[str]
    streams: list[str]
    enabled: bool = False
    fallback: str = "rest-cache"
    credentials_required: bool = False
    user_data_stream: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "symbols": [symbol.upper() for symbol in self.symbols],
            "streams": self.streams,
            "enabled": self.enabled,
            "fallback": self.fallback,
            "credentials_required": self.credentials_required,
            "user_data_stream": self.user_data_stream,
            "live_trading_enabled": False,
        }


def build_public_ws_plan(symbols: list[str], streams: list[str] | None = None, *, enabled: bool = False) -> dict[str, object]:
    requested = streams or list(PUBLIC_WS_STREAMS)
    allowed = [stream for stream in requested if stream in PUBLIC_WS_STREAMS]
    return PublicWebSocketPlan(symbols=symbols, streams=allowed, enabled=enabled).to_dict()
