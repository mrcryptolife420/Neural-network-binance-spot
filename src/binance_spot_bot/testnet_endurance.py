from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class TestnetEnduranceGuard:
    max_orders: int
    live_urls_allowed: bool = False
    orders_seen: int = 0
    unresolved_orders: list[str] = field(default_factory=list)

    def allow_order(self, base_url: str) -> tuple[bool, str]:
        if "api.binance.com" in base_url and not self.live_urls_allowed:
            return False, "live URL is not allowed in endurance mode"
        if self.orders_seen >= self.max_orders:
            return False, "max endurance orders reached"
        self.orders_seen += 1
        return True, "testnet order budget available"

    def record_unresolved(self, client_order_id: str) -> None:
        self.unresolved_orders.append(client_order_id)

    def reconcile_order(self, client_order_id: str, status: str) -> None:
        if status in {"FILLED", "CANCELED", "REJECTED", "EXPIRED"} and client_order_id in self.unresolved_orders:
            self.unresolved_orders.remove(client_order_id)

    def cancel_open_orders(self) -> list[str]:
        canceled = list(self.unresolved_orders)
        self.unresolved_orders.clear()
        return canceled

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
