from __future__ import annotations

import uuid
from decimal import Decimal, ROUND_DOWN

from .audit import AuditLog
from .binance import BinanceAPIError, BinanceSpotAdapter
from .config import BotSettings
from .demo_spot import evaluate_demo_trading_gate
from .exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from .types import (
    ExecutionResult,
    MarketState,
    OrderRequest,
    OrderSide,
    RiskDecision,
    RiskDecisionType,
    SymbolFilters,
    TradingMode,
)


class ExecutionBlocked(RuntimeError):
    pass


def quantize_down(value: Decimal, step: Decimal) -> Decimal:
    if step <= 0:
        return value
    return (value / step).to_integral_value(rounding=ROUND_DOWN) * step


class ExecutionEngine:
    def __init__(
        self,
        settings: BotSettings,
        audit_log: AuditLog,
        adapter: BinanceSpotAdapter | None = None,
        demo_trading_armed: bool = False,
        max_demo_orders_per_session: int = 25,
    ):
        self.settings = settings
        self.audit_log = audit_log
        self.adapter = adapter
        self.demo_trading_armed = demo_trading_armed
        self.max_demo_orders_per_session = max_demo_orders_per_session
        self.demo_orders_sent = 0

    def execute(
        self,
        decision: RiskDecision,
        market: MarketState,
        filters: SymbolFilters,
    ) -> ExecutionResult:
        if decision.decision != RiskDecisionType.ALLOW or decision.intent is None:
            self.audit_log.emit("execution", "blocked", {"reason": decision.reason})
            return ExecutionResult(self.settings.trading_mode, "BLOCKED", None, {"reason": decision.reason})

        order = self._build_order(decision, market, filters)
        self.audit_log.emit("execution", "order_intent_created", {"order": order})

        if self.settings.trading_mode == TradingMode.DISABLED:
            return ExecutionResult(TradingMode.DISABLED, "DISABLED", order, {})
        if self.settings.trading_mode == TradingMode.PAPER:
            return self._paper_fill(order, market)
        if self.settings.trading_mode == TradingMode.TESTNET:
            if self.adapter is None:
                raise ExecutionBlocked("testnet execution requires Binance adapter")
            if self.settings.exchange_profile == BINANCE_DEMO_SPOT_PROFILE:
                gate = evaluate_demo_trading_gate(
                    profile=self.settings.exchange_profile,
                    base_url=self.settings.active_base_url,
                    has_credentials=bool(self.settings.binance_api_key and self.settings.binance_api_secret),
                    connection_ok=True,
                    armed=self.demo_trading_armed,
                    live_trading_enabled=self.settings.live_trading_enabled,
                    kill_switch=self.settings.kill_switch,
                    risk_allowed=True,
                    filters_loaded=filters.status == "TRADING",
                    max_orders_ok=self.demo_orders_sent < self.max_demo_orders_per_session,
                )
                self.audit_log.emit("execution", "demo_trading_gate", gate.to_dict())
                if not gate.allowed:
                    return ExecutionResult(TradingMode.TESTNET, "BLOCKED", order, {"reason": gate.reason, "gate": gate.to_dict()})
                try:
                    test_response = self.adapter.test_order(order)
                    response = self.adapter.place_order(order)
                except (BinanceAPIError, Exception) as exc:
                    payload = {
                        "error": str(exc),
                        "status": exc.status if isinstance(exc, BinanceAPIError) else None,
                        "payload": exc.payload if isinstance(exc, BinanceAPIError) else None,
                    }
                    self.audit_log.emit("execution", "demo_order_rejected", payload)
                    return ExecutionResult(TradingMode.TESTNET, "REJECTED", order, payload)
                self.demo_orders_sent += 1
                response = {"test_order": test_response, **response}
                self.audit_log.emit("execution", "demo_order_submitted", {"response": response})
                return ExecutionResult(TradingMode.TESTNET, str(response.get("status", "DEMO_ORDER_ACCEPTED")), order, response)
            response = self.adapter.test_order(order)
            self.audit_log.emit("execution", "testnet_test_order_accepted", {"response": response})
            return ExecutionResult(TradingMode.TESTNET, "TEST_ORDER_ACCEPTED", order, response)
        if self.settings.trading_mode == TradingMode.LIVE:
            self.settings.validate_live_readiness()
            raise ExecutionBlocked("live order placement requires a separate manual implementation step")
        raise ExecutionBlocked(f"unsupported trading mode: {self.settings.trading_mode}")

    def _build_order(
        self,
        decision: RiskDecision,
        market: MarketState,
        filters: SymbolFilters,
    ) -> OrderRequest:
        assert decision.intent is not None
        quote_size = decision.intent.quote_size
        approx_qty = quote_size / market.last_price
        quantity = quantize_down(approx_qty, filters.step_size)
        if quantity < filters.min_qty:
            raise ExecutionBlocked("quantity below LOT_SIZE minQty")
        if quantity > filters.max_qty:
            raise ExecutionBlocked("quantity above LOT_SIZE maxQty")
        notional = quantity * market.last_price
        if notional < filters.min_notional:
            raise ExecutionBlocked("order notional below NOTIONAL minNotional")
        if decision.intent.side == OrderSide.SELL and quantity <= 0:
            raise ExecutionBlocked("sell quantity must be positive")
        return OrderRequest(
            symbol=decision.intent.symbol,
            side=decision.intent.side,
            order_type=decision.intent.order_type,
            quantity=quantity,
            client_order_id=f"spotbot-{uuid.uuid4().hex[:24]}",
        )

    def _paper_fill(self, order: OrderRequest, market: MarketState) -> ExecutionResult:
        response = {
            "symbol": order.symbol,
            "side": order.side.value,
            "status": "FILLED",
            "paper": True,
            "price": str(market.last_price),
            "executedQty": str(order.quantity or Decimal("0")),
        }
        self.audit_log.emit("execution", "paper_order_filled", response)
        return ExecutionResult(TradingMode.PAPER, "FILLED", order, response)
