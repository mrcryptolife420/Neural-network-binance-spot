from __future__ import annotations

import hashlib
import hmac
import json
import time
from decimal import Decimal
from typing import Any
from urllib import parse, request
from urllib.error import HTTPError, URLError

from .config import BotSettings, ConfigError
from .types import OrderRequest, SymbolFilters


class BinanceAPIError(RuntimeError):
    def __init__(self, message: str, status: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status = status
        self.payload = payload


class BinanceSpotAdapter:
    def __init__(self, settings: BotSettings):
        self.settings = settings
        self.base_url = settings.active_base_url
        self._last_request_ms = 0

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        signed: bool = False,
    ) -> Any:
        params = dict(params or {})
        headers = {"User-Agent": "neural-network-binance-spot/0.1"}
        if signed:
            if not self.settings.binance_api_key or not self.settings.binance_api_secret:
                raise ConfigError("Signed Binance request requires API credentials")
            params.setdefault("timestamp", self.server_time())
            params.setdefault("recvWindow", 5000)
            params["signature"] = self._sign(params)
            headers["X-MBX-APIKEY"] = self.settings.binance_api_key

        query = parse.urlencode(params, doseq=True)
        url = f"{self.base_url}{path}"
        data = None
        if method in {"GET", "DELETE"} and query:
            url = f"{url}?{query}"
        elif query:
            data = query.encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        self._pace_requests()
        req = request.Request(url, data=data, method=method, headers=headers)
        try:
            with request.urlopen(req, timeout=10) as response:
                raw = response.read().decode("utf-8")
                if not raw:
                    return {}
                return json.loads(raw)
        except HTTPError as exc:
            raw_payload = exc.read().decode("utf-8", errors="replace")
            payload: Any
            try:
                payload = json.loads(raw_payload)
            except json.JSONDecodeError:
                payload = raw_payload
            if exc.code in {418, 429}:
                raise BinanceAPIError("Binance rate limit or IP ban response", exc.code, payload) from exc
            raise BinanceAPIError("Binance API request failed", exc.code, payload) from exc
        except URLError as exc:
            raise BinanceAPIError(f"Binance network error: {exc.reason}") from exc

    def _pace_requests(self) -> None:
        now = int(time.time() * 1000)
        elapsed = now - self._last_request_ms
        if elapsed < 50:
            time.sleep((50 - elapsed) / 1000)
        self._last_request_ms = int(time.time() * 1000)

    def _sign(self, params: dict[str, Any]) -> str:
        payload = parse.urlencode(params, doseq=True)
        return hmac.new(
            self.settings.binance_api_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def server_time(self) -> int:
        if self.settings.trading_mode.value in {"testnet", "live"}:
            result = self._request("GET", "/api/v3/time")
            return int(result["serverTime"])
        return int(time.time() * 1000)

    def get_exchange_info(self, symbols: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"showPermissionSets": "false"}
        if symbols:
            if len(symbols) == 1:
                params["symbol"] = symbols[0]
            else:
                params["symbols"] = json.dumps(symbols)
        return self._request("GET", "/api/v3/exchangeInfo", params=params)

    def get_symbol_filters(self, symbol: str) -> SymbolFilters:
        info = self.get_exchange_info([symbol])
        symbol_info = info["symbols"][0]
        filters = {item["filterType"]: item for item in symbol_info["filters"]}
        price_filter = filters["PRICE_FILTER"]
        lot_size = filters["LOT_SIZE"]
        notional = filters.get("NOTIONAL") or filters.get("MIN_NOTIONAL") or {}
        market_lot = filters.get("MARKET_LOT_SIZE", {})
        return SymbolFilters(
            symbol=symbol_info["symbol"],
            status=symbol_info["status"],
            tick_size=Decimal(price_filter["tickSize"]),
            step_size=Decimal(lot_size["stepSize"]),
            min_qty=Decimal(lot_size["minQty"]),
            max_qty=Decimal(lot_size["maxQty"]),
            min_notional=Decimal(notional.get("minNotional", "0")),
            market_max_qty=Decimal(market_lot["maxQty"]) if market_lot.get("maxQty") else None,
        )

    def get_klines(
        self,
        symbol: str,
        interval: str,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 500,
    ) -> list[list[Any]]:
        params: dict[str, Any] = {"symbol": symbol, "interval": interval, "limit": limit}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        return self._request("GET", "/api/v3/klines", params=params)

    def get_order_book(self, symbol: str, depth: int = 100) -> dict[str, Any]:
        return self._request("GET", "/api/v3/depth", params={"symbol": symbol, "limit": depth})

    def get_account_state(self) -> dict[str, Any]:
        return self._request("GET", "/api/v3/account", signed=True)

    def test_order(self, order: OrderRequest) -> dict[str, Any]:
        return self._request("POST", "/api/v3/order/test", params=self._order_params(order), signed=True)

    def place_order(self, order: OrderRequest) -> dict[str, Any]:
        self.settings.validate_startup()
        if self.settings.trading_mode.value == "live":
            self.settings.validate_live_readiness()
        return self._request("POST", "/api/v3/order", params=self._order_params(order), signed=True)

    def cancel_order(self, symbol: str, order_id: int) -> dict[str, Any]:
        return self._request(
            "DELETE",
            "/api/v3/order",
            params={"symbol": symbol, "orderId": order_id},
            signed=True,
        )

    def get_order(self, symbol: str, order_id: int) -> dict[str, Any]:
        return self._request(
            "GET",
            "/api/v3/order",
            params={"symbol": symbol, "orderId": order_id},
            signed=True,
        )

    def _order_params(self, order: OrderRequest) -> dict[str, Any]:
        params: dict[str, Any] = {
            "symbol": order.symbol,
            "side": order.side.value,
            "type": order.order_type.value,
        }
        if order.quantity is not None:
            params["quantity"] = str(order.quantity)
        if order.quote_order_qty is not None:
            params["quoteOrderQty"] = str(order.quote_order_qty)
        if order.price is not None:
            params["price"] = str(order.price)
        if order.client_order_id:
            params["newClientOrderId"] = order.client_order_id
        return params

