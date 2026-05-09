from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any

from .user_data_stream import ExecutionReportEvent


TERMINAL_STATUSES = {"FILLED", "CANCELED", "REJECTED", "EXPIRED"}


@dataclass
class OrderLifecycle:
    client_order_id: str
    symbol: str
    side: str
    status: str = "INTENT"
    order_id: int | None = None
    filled_quantity: Decimal = Decimal("0")
    last_price: Decimal = Decimal("0")
    events: list[dict[str, Any]] = field(default_factory=list)
    needs_reconciliation: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["filled_quantity"] = str(self.filled_quantity)
        payload["last_price"] = str(self.last_price)
        return payload


class OrderLifecycleStore:
    def __init__(self) -> None:
        self.orders: dict[str, OrderLifecycle] = {}

    def record_intent(self, client_order_id: str, symbol: str, side: str) -> OrderLifecycle:
        lifecycle = OrderLifecycle(client_order_id=client_order_id, symbol=symbol, side=side)
        lifecycle.events.append({"type": "INTENT", "status": "INTENT"})
        self.orders[client_order_id] = lifecycle
        return lifecycle

    def mark_submitted_unknown(self, client_order_id: str, message: str) -> OrderLifecycle:
        lifecycle = self.orders.setdefault(
            client_order_id,
            OrderLifecycle(client_order_id=client_order_id, symbol="", side="", status="UNKNOWN"),
        )
        lifecycle.status = "UNKNOWN"
        lifecycle.needs_reconciliation = True
        lifecycle.events.append({"type": "UNKNOWN", "message": message})
        return lifecycle

    def apply_execution_report(self, event: ExecutionReportEvent) -> OrderLifecycle:
        lifecycle = self.orders.setdefault(
            event.client_order_id,
            OrderLifecycle(event.client_order_id, event.symbol, event.side),
        )
        lifecycle.symbol = event.symbol
        lifecycle.side = event.side
        lifecycle.status = event.order_status
        lifecycle.order_id = event.order_id
        lifecycle.filled_quantity = event.cumulative_filled_quantity
        lifecycle.last_price = event.last_executed_price
        lifecycle.needs_reconciliation = event.order_status not in TERMINAL_STATUSES and event.execution_type not in {"NEW", "TRADE"}
        lifecycle.events.append(
            {
                "type": event.execution_type,
                "status": event.order_status,
                "event_time_ms": event.event_time_ms,
                "filled_quantity": str(event.cumulative_filled_quantity),
                "last_price": str(event.last_executed_price),
                "reject_reason": event.reject_reason,
            }
        )
        return lifecycle

    def list_recent(self, limit: int = 20) -> list[dict[str, Any]]:
        return [order.to_dict() for order in list(self.orders.values())[-limit:]]
