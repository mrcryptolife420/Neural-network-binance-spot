from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal

from .execution import quantize_down
from .order_lifecycle import OrderLifecycleStore
from .types import OrderSide, SymbolFilters


@dataclass(frozen=True)
class ManualDemoTradeRequest:
    symbol: str
    side: OrderSide
    quote_size: Decimal
    price: Decimal
    quote_balance: Decimal
    base_balance: Decimal = Decimal("0")
    fee_bps: Decimal = Decimal("10")
    slippage_bps: Decimal = Decimal("5")
    confirmed_demo_only: bool = False


@dataclass(frozen=True)
class ManualDemoTradePreview:
    allowed: bool
    reason: str
    quantity: Decimal
    notional: Decimal
    estimated_fee: Decimal
    estimated_price: Decimal

    def to_dict(self) -> dict[str, str | bool]:
        payload = asdict(self)
        return {key: (str(value) if isinstance(value, Decimal) else value) for key, value in payload.items()}


@dataclass(frozen=True)
class ManualDemoTradeResult:
    status: str
    preview: ManualDemoTradePreview
    fill: dict[str, str]


def preview_manual_demo_trade(request: ManualDemoTradeRequest, filters: SymbolFilters) -> ManualDemoTradePreview:
    if not request.confirmed_demo_only:
        return _blocked("demo confirmation required", request.price)
    if request.quote_size <= 0:
        return _blocked("quote size must be positive", request.price)
    price_multiplier = Decimal("1") + (request.slippage_bps / Decimal("10000"))
    fill_price = request.price * price_multiplier if request.side == OrderSide.BUY else request.price / price_multiplier
    quantity = quantize_down(request.quote_size / fill_price, filters.step_size)
    notional = quantity * fill_price
    fee = notional * request.fee_bps / Decimal("10000")
    if quantity < filters.min_qty:
        return _blocked("quantity below LOT_SIZE minQty", fill_price)
    if notional < filters.min_notional:
        return _blocked("order notional below NOTIONAL minNotional", fill_price)
    if request.side == OrderSide.BUY and request.quote_balance < notional + fee:
        return _blocked("insufficient quote balance", fill_price)
    if request.side == OrderSide.SELL and request.base_balance < quantity:
        return _blocked("insufficient base balance", fill_price)
    return ManualDemoTradePreview(True, "risk checks passed", quantity, notional, fee, fill_price)


def execute_manual_demo_trade(
    request: ManualDemoTradeRequest,
    filters: SymbolFilters,
    lifecycle: OrderLifecycleStore | None = None,
) -> ManualDemoTradeResult:
    preview = preview_manual_demo_trade(request, filters)
    if not preview.allowed:
        return ManualDemoTradeResult("BLOCKED", preview, {})
    lifecycle = lifecycle or OrderLifecycleStore()
    client_order_id = f"manual-demo-{request.symbol.lower()}-{request.side.value.lower()}"
    lifecycle.record_intent(client_order_id, request.symbol, request.side.value)
    fill = {
        "client_order_id": client_order_id,
        "origin": "manual_demo",
        "symbol": request.symbol,
        "side": request.side.value,
        "quantity": str(preview.quantity),
        "price": str(preview.estimated_price),
        "notional": str(preview.notional),
        "fee": str(preview.estimated_fee),
        "status": "PAPER_FILLED",
    }
    return ManualDemoTradeResult("PAPER_FILLED", preview, fill)


def _blocked(reason: str, price: Decimal) -> ManualDemoTradePreview:
    return ManualDemoTradePreview(False, reason, Decimal("0"), Decimal("0"), Decimal("0"), price)
