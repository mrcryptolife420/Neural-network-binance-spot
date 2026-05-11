from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from .audit import AuditLog
from .binance import BinanceAPIError, BinanceSpotAdapter
from .config import BotSettings
from .demo_spot import DEMO_SPOT_BASE_URL, evaluate_demo_trading_gate, normalize_base_url
from .exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from .execution import ExecutionBlocked, ExecutionEngine
from .order_lifecycle import OrderLifecycleStore
from .redaction import redact_payload
from .types import (
    MarketState,
    OrderRequest,
    OrderSide,
    OrderType,
    RiskDecision,
    RiskDecisionType,
    SymbolFilters,
    TradeIntent,
    TradingMode,
)


@dataclass(frozen=True)
class SandboxIntent:
    symbol: str
    side: OrderSide
    quote_size: Decimal
    last_price: Decimal = Decimal("100")
    order_type: OrderType = OrderType.MARKET

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["side"] = self.side.value
        payload["quote_size"] = str(self.quote_size)
        payload["last_price"] = str(self.last_price)
        payload["order_type"] = self.order_type.value
        return payload


@dataclass(frozen=True)
class SandboxOrderPreview:
    intent: SandboxIntent
    order: OrderRequest
    filters: SymbolFilters
    market: MarketState
    risk_decision: RiskDecision
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                "intent": self.intent.to_dict(),
                "order": _order_to_dict(self.order),
                "filters": _filters_to_dict(self.filters),
                "market": _market_to_dict(self.market),
                "risk_decision": {
                    "decision": self.risk_decision.decision.value,
                    "reason": self.risk_decision.reason,
                },
                "live_trading_enabled": False,
            }
        )


@dataclass(frozen=True)
class SandboxDrillResult:
    action: str
    status: str
    reason: str
    preview: dict[str, Any] | None = None
    response: dict[str, Any] | None = None
    lifecycle: list[dict[str, Any]] | None = None
    evidence_path: str = ""
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class DemoExecutionSandbox:
    def __init__(
        self,
        settings: BotSettings,
        adapter: BinanceSpotAdapter | None = None,
        lifecycle: OrderLifecycleStore | None = None,
        audit: AuditLog | None = None,
    ) -> None:
        self.settings = settings
        self.adapter = adapter
        self.lifecycle = lifecycle or OrderLifecycleStore()
        self.audit = audit or AuditLog(settings.audit_log_path)

    def preview(self, intent: SandboxIntent, filters: SymbolFilters | None = None) -> SandboxDrillResult:
        try:
            preview = self._preview(intent, filters)
        except ExecutionBlocked as exc:
            return self._write_result(SandboxDrillResult("preview", "BLOCKED", str(exc)))
        client_order_id = preview.order.client_order_id or ""
        self.lifecycle.record_intent(client_order_id, preview.order.symbol, preview.order.side.value)
        self.lifecycle.orders[client_order_id].events.append({"type": "PREVIEW_CREATED", "status": "PREVIEW"})
        return self._write_result(
            SandboxDrillResult(
                "preview",
                "PREVIEW_READY",
                "order preview created",
                preview=preview.to_dict(),
                lifecycle=self.lifecycle.list_recent(),
            )
        )

    def test_order_only(self, intent: SandboxIntent, filters: SymbolFilters | None = None) -> SandboxDrillResult:
        preview_result = self.preview(intent, filters)
        if preview_result.status != "PREVIEW_READY" or not preview_result.preview:
            return preview_result
        blocked = self._signed_order_block_reason(require_armed=False, require_kill_switch_off=False)
        if blocked:
            return self._write_result(
                SandboxDrillResult("test_order", "BLOCKED", blocked, preview=preview_result.preview, lifecycle=self.lifecycle.list_recent())
            )
        if self.adapter is None:
            return self._write_result(
                SandboxDrillResult("test_order", "BLOCKED", "adapter required for signed test order", preview=preview_result.preview, lifecycle=self.lifecycle.list_recent())
            )
        order = self._order_from_preview(preview_result.preview)
        try:
            response = self.adapter.test_order(order)
            self.lifecycle.orders[order.client_order_id or ""].events.append({"type": "TEST_ORDER", "status": "ACCEPTED"})
            status = "TEST_ORDER_ACCEPTED"
            reason = "test order accepted"
        except (BinanceAPIError, Exception) as exc:
            response = _exception_payload(exc)
            self.lifecycle.mark_submitted_unknown(order.client_order_id or "", str(exc))
            status = "REJECTED"
            reason = str(exc)
        return self._write_result(
            SandboxDrillResult(
                "test_order",
                status,
                reason,
                preview=preview_result.preview,
                response=response,
                lifecycle=self.lifecycle.list_recent(),
            )
        )

    def place_demo_order(
        self,
        intent: SandboxIntent,
        *,
        confirm_demo_order: bool,
        armed: bool,
        filters: SymbolFilters | None = None,
    ) -> SandboxDrillResult:
        preview_result = self.preview(intent, filters)
        if preview_result.status != "PREVIEW_READY" or not preview_result.preview:
            return preview_result
        if not confirm_demo_order:
            return self._write_result(
                SandboxDrillResult("place_order", "BLOCKED", "confirm demo order first", preview=preview_result.preview, lifecycle=self.lifecycle.list_recent())
            )
        blocked = self._signed_order_block_reason(require_armed=armed, require_kill_switch_off=True)
        if blocked:
            return self._write_result(
                SandboxDrillResult("place_order", "BLOCKED", blocked, preview=preview_result.preview, lifecycle=self.lifecycle.list_recent())
            )
        if self.adapter is None:
            return self._write_result(
                SandboxDrillResult("place_order", "BLOCKED", "adapter required for demo order placement", preview=preview_result.preview, lifecycle=self.lifecycle.list_recent())
            )
        order = self._order_from_preview(preview_result.preview)
        try:
            test_response = self.adapter.test_order(order)
            response = self.adapter.place_order(order)
            response = {"test_order": test_response, **response}
            self.lifecycle.apply_order_payload({**response, "clientOrderId": order.client_order_id, "symbol": order.symbol, "side": order.side.value})
            status = str(response.get("status", "DEMO_ORDER_SUBMITTED"))
            reason = "demo order submitted"
        except (BinanceAPIError, Exception) as exc:
            response = _exception_payload(exc)
            self.lifecycle.mark_submitted_unknown(order.client_order_id or "", str(exc))
            status = "REJECTED"
            reason = str(exc)
        return self._write_result(
            SandboxDrillResult("place_order", status, reason, preview=preview_result.preview, response=response, lifecycle=self.lifecycle.list_recent())
        )

    def query_order(self, symbol: str, *, order_id: int | None = None, client_order_id: str | None = None) -> SandboxDrillResult:
        blocked = self._signed_order_block_reason(require_armed=False, require_kill_switch_off=False)
        if blocked:
            return self._write_result(SandboxDrillResult("query_order", "BLOCKED", blocked, lifecycle=self.lifecycle.list_recent()))
        if self.adapter is None:
            return self._write_result(SandboxDrillResult("query_order", "BLOCKED", "adapter required for order query", lifecycle=self.lifecycle.list_recent()))
        try:
            response = self.adapter.query_order(symbol, order_id=order_id, client_order_id=client_order_id)
            lifecycle = self.lifecycle.apply_order_payload(response)
            status = lifecycle.status
            reason = "order queried"
        except (BinanceAPIError, Exception) as exc:
            response = _exception_payload(exc)
            status = "REJECTED"
            reason = str(exc)
        return self._write_result(SandboxDrillResult("query_order", status, reason, response=response, lifecycle=self.lifecycle.list_recent()))

    def cancel_order(self, symbol: str, order_id: int, *, confirm_cancel: bool) -> SandboxDrillResult:
        if not confirm_cancel:
            return self._write_result(SandboxDrillResult("cancel_order", "BLOCKED", "confirm cancel first", lifecycle=self.lifecycle.list_recent()))
        blocked = self._signed_order_block_reason(require_armed=False, require_kill_switch_off=False)
        if blocked:
            return self._write_result(SandboxDrillResult("cancel_order", "BLOCKED", blocked, lifecycle=self.lifecycle.list_recent()))
        if self.adapter is None:
            return self._write_result(SandboxDrillResult("cancel_order", "BLOCKED", "adapter required for order cancel", lifecycle=self.lifecycle.list_recent()))
        try:
            response = self.adapter.cancel_order(symbol, order_id)
            lifecycle = self.lifecycle.apply_order_payload(response)
            status = lifecycle.status
            reason = "order cancel requested"
        except (BinanceAPIError, Exception) as exc:
            response = _exception_payload(exc)
            status = "REJECTED"
            reason = str(exc)
        return self._write_result(SandboxDrillResult("cancel_order", status, reason, response=response, lifecycle=self.lifecycle.list_recent()))

    def latest_report(self) -> dict[str, Any]:
        path = self._latest_path()
        if not path.exists():
            return {"status": "missing", "live_trading_enabled": False, "path": str(path)}
        return json.loads(path.read_text(encoding="utf-8"))

    def _preview(self, intent: SandboxIntent, filters: SymbolFilters | None) -> SandboxOrderPreview:
        market = MarketState(symbol=intent.symbol, last_price=intent.last_price, bid=intent.last_price, ask=intent.last_price)
        active_filters = filters or default_filters(intent.symbol)
        risk_decision = RiskDecision(
            RiskDecisionType.ALLOW,
            "manual sandbox intent",
            TradeIntent(
                symbol=intent.symbol,
                side=intent.side,
                quote_size=intent.quote_size,
                order_type=intent.order_type,
                max_slippage_bps=Decimal("10"),
            ),
        )
        engine = ExecutionEngine(self.settings, self.audit, adapter=None, demo_trading_armed=False)
        order = engine._build_order(risk_decision, market, active_filters)
        return SandboxOrderPreview(intent, order, active_filters, market, risk_decision)

    def _signed_order_block_reason(self, *, require_armed: bool, require_kill_switch_off: bool) -> str:
        if self.settings.trading_mode == TradingMode.LIVE or self.settings.live_trading_enabled:
            return "live trading blocked"
        if self.settings.exchange_profile != BINANCE_DEMO_SPOT_PROFILE:
            return "Binance Demo Spot profile required"
        if normalize_base_url(self.settings.active_base_url) != DEMO_SPOT_BASE_URL:
            return "Binance Demo Spot base URL required"
        if not (self.settings.binance_api_key and self.settings.binance_api_secret):
            return "Demo Spot credentials required"
        if require_kill_switch_off and self.settings.kill_switch:
            return "kill switch must be off for demo order placement"
        if require_armed is False and require_kill_switch_off:
            return "demo trading must be armed"
        return ""

    def _write_result(self, result: SandboxDrillResult) -> SandboxDrillResult:
        payload = result.to_dict()
        out_dir = self.settings.data_dir / "evidence" / "demo-execution"
        out_dir.mkdir(parents=True, exist_ok=True)
        latest = self._latest_path()
        stamped = out_dir / f"demo_execution_drill_{int(time.time() * 1000)}.json"
        latest.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        stamped.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        self.audit.emit("demo_execution_sandbox", result.action, payload)
        return SandboxDrillResult(**{**payload, "evidence_path": str(latest)})

    def _latest_path(self) -> Path:
        return self.settings.data_dir / "evidence" / "demo-execution" / "demo_execution_drill.json"

    @staticmethod
    def _order_from_preview(preview: dict[str, Any]) -> OrderRequest:
        order = preview["order"]
        return OrderRequest(
            symbol=order["symbol"],
            side=OrderSide(order["side"]),
            order_type=OrderType(order["order_type"]),
            quantity=Decimal(str(order["quantity"])) if order.get("quantity") else None,
            quote_order_qty=Decimal(str(order["quote_order_qty"])) if order.get("quote_order_qty") else None,
            price=Decimal(str(order["price"])) if order.get("price") else None,
            client_order_id=order.get("client_order_id"),
        )


def default_filters(symbol: str) -> SymbolFilters:
    return SymbolFilters(
        symbol=symbol,
        status="TRADING",
        tick_size=Decimal("0.01"),
        step_size=Decimal("0.000001"),
        min_qty=Decimal("0.000001"),
        max_qty=Decimal("1000"),
        min_notional=Decimal("5"),
    )


def intent_from_values(symbol: str, side: str, quote_size: str | Decimal, last_price: str | Decimal = "100") -> SandboxIntent:
    return SandboxIntent(symbol.upper(), OrderSide(side.upper()), Decimal(str(quote_size)), Decimal(str(last_price)))


def _order_to_dict(order: OrderRequest) -> dict[str, Any]:
    return {
        "symbol": order.symbol,
        "side": order.side.value,
        "order_type": order.order_type.value,
        "quantity": str(order.quantity) if order.quantity is not None else None,
        "quote_order_qty": str(order.quote_order_qty) if order.quote_order_qty is not None else None,
        "price": str(order.price) if order.price is not None else None,
        "client_order_id": order.client_order_id,
    }


def _filters_to_dict(filters: SymbolFilters) -> dict[str, Any]:
    return {key: str(value) for key, value in asdict(filters).items()}


def _market_to_dict(market: MarketState) -> dict[str, Any]:
    return {
        "symbol": market.symbol,
        "last_price": str(market.last_price),
        "bid": str(market.bid) if market.bid is not None else None,
        "ask": str(market.ask) if market.ask is not None else None,
    }


def _exception_payload(exc: Exception) -> dict[str, Any]:
    return redact_payload(
        {
            "error": str(exc),
            "status": exc.status if isinstance(exc, BinanceAPIError) else None,
            "payload": exc.payload if isinstance(exc, BinanceAPIError) else None,
        }
    )
