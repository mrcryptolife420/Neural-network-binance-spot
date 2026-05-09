from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .binance import BinanceAPIError, BinanceSpotAdapter
from .config import BotSettings
from .exchange_profiles import CredentialProfile, profile_for
from .redaction import redact_payload
from .types import OrderRequest, OrderSide, OrderType


@dataclass(frozen=True)
class ConnectivityCheck:
    name: str
    status: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "details": redact_payload(self.details),
        }


def check_public_market_data(settings: BotSettings, symbol: str, adapter: BinanceSpotAdapter | None = None) -> ConnectivityCheck:
    profile = profile_for(settings.exchange_profile)
    if not profile.requires_credentials:
        return ConnectivityCheck("public_market_data", "ok", "No signed credentials required", {"profile": profile.name})
    try:
        adapter = adapter or BinanceSpotAdapter(settings)
        payload = adapter.get_order_book(symbol, depth=5)
        return ConnectivityCheck("public_market_data", "ok", "public market data reachable", {"lastUpdateId": payload.get("lastUpdateId")})
    except (BinanceAPIError, OSError, ValueError) as exc:
        return ConnectivityCheck("public_market_data", "degraded", "public market data check failed", {"error": str(exc)})


def check_server_time(settings: BotSettings, adapter: BinanceSpotAdapter | None = None) -> ConnectivityCheck:
    profile = profile_for(settings.exchange_profile)
    if not profile.requires_credentials:
        return ConnectivityCheck("server_time", "ok", "local demo does not require server time", {})
    try:
        adapter = adapter or BinanceSpotAdapter(settings)
        server_ms = adapter.server_time()
        local_ms = int(time.time() * 1000)
        drift = abs(local_ms - server_ms)
        status = "ok" if drift < 2_000 else "degraded"
        return ConnectivityCheck("server_time", status, "server time checked", {"drift_ms": drift, "server_time_ms": server_ms})
    except (BinanceAPIError, OSError, ValueError) as exc:
        return ConnectivityCheck("server_time", "degraded", "server time check failed", {"error": str(exc)})


def check_exchange_info(settings: BotSettings, symbol: str, adapter: BinanceSpotAdapter | None = None) -> ConnectivityCheck:
    profile = profile_for(settings.exchange_profile)
    if not profile.requires_credentials:
        return ConnectivityCheck("exchange_info", "ok", "local demo uses default filters", {"symbol": symbol})
    try:
        adapter = adapter or BinanceSpotAdapter(settings)
        filters = adapter.get_symbol_filters(symbol)
        return ConnectivityCheck(
            "exchange_info",
            "ok",
            "exchange filters loaded",
            {
                "symbol": filters.symbol,
                "status": filters.status,
                "tick_size": str(filters.tick_size),
                "step_size": str(filters.step_size),
                "min_notional": str(filters.min_notional),
            },
        )
    except (BinanceAPIError, OSError, ValueError, KeyError) as exc:
        return ConnectivityCheck("exchange_info", "degraded", "exchange info check failed", {"error": str(exc)})


def check_signed_account(settings: BotSettings, adapter: BinanceSpotAdapter | None = None) -> ConnectivityCheck:
    profile = profile_for(settings.exchange_profile)
    if not profile.requires_credentials:
        return ConnectivityCheck("signed_account", "ok", "No signed credentials required", {"profile": profile.name})
    if not settings.binance_api_key or not settings.binance_api_secret:
        return ConnectivityCheck("signed_account", "needs_credentials", "needs credentials", {"profile": profile.name})
    try:
        adapter = adapter or BinanceSpotAdapter(settings)
        payload = adapter.get_account_state()
        return ConnectivityCheck(
            "signed_account",
            "ok",
            "signed account check ok",
            {"canTrade": payload.get("canTrade"), "accountType": payload.get("accountType")},
        )
    except Exception as exc:
        return ConnectivityCheck("signed_account", "degraded", "signed account check failed", {"error": str(exc)})


def check_test_order_capability(settings: BotSettings, symbol: str, adapter: BinanceSpotAdapter | None = None) -> ConnectivityCheck:
    profile = profile_for(settings.exchange_profile)
    if not profile.requires_credentials:
        return ConnectivityCheck("test_order", "blocked", "local demo never sends signed test orders", {})
    if not settings.binance_api_key or not settings.binance_api_secret:
        return ConnectivityCheck("test_order", "needs_credentials", "needs credentials", {})
    try:
        adapter = adapter or BinanceSpotAdapter(settings)
        request = OrderRequest(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quote_order_qty=None,
            quantity=None,
        )
        return ConnectivityCheck("test_order", "ready", "test-order endpoint available but not called by default", {"symbol": request.symbol})
    except Exception as exc:
        return ConnectivityCheck("test_order", "degraded", "test order readiness failed", {"error": str(exc)})


def connectivity_report(settings: BotSettings, symbol: str, adapter: BinanceSpotAdapter | None = None) -> dict[str, Any]:
    checks = [
        check_public_market_data(settings, symbol, adapter),
        check_server_time(settings, adapter),
        check_exchange_info(settings, symbol, adapter),
        check_signed_account(settings, adapter),
        check_test_order_capability(settings, symbol, adapter),
    ]
    status = "ok"
    if any(check.status in {"needs_credentials", "degraded"} for check in checks):
        status = "degraded"
    if any(check.status == "unhealthy" for check in checks):
        status = "unhealthy"
    profile = profile_for(settings.exchange_profile)
    return {
        "status": status,
        "profile": profile.to_dict(),
        "base_url": settings.active_base_url,
        "live_trading_enabled": settings.live_trading_enabled,
        "checks": [check.to_dict() for check in checks],
        "checked_at_ms": int(time.time() * 1000),
    }
