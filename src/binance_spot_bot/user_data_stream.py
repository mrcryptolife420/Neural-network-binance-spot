from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class AccountPositionEvent:
    event_time_ms: int
    update_time_ms: int
    balances: list[dict[str, Decimal]]


@dataclass(frozen=True)
class BalanceUpdateEvent:
    event_time_ms: int
    asset: str
    delta: Decimal
    clear_time_ms: int


@dataclass(frozen=True)
class ExecutionReportEvent:
    event_time_ms: int
    symbol: str
    client_order_id: str
    side: str
    order_type: str
    execution_type: str
    order_status: str
    reject_reason: str
    order_id: int
    last_executed_quantity: Decimal
    cumulative_filled_quantity: Decimal
    last_executed_price: Decimal
    commission_amount: Decimal
    commission_asset: str | None
    transaction_time_ms: int


@dataclass(frozen=True)
class ListStatusEvent:
    event_time_ms: int
    symbol: str
    order_list_id: int
    list_status_type: str
    list_order_status: str
    reject_reason: str


def parse_user_data_message(payload: dict[str, Any]) -> AccountPositionEvent | BalanceUpdateEvent | ExecutionReportEvent | ListStatusEvent:
    event = payload.get("event", payload)
    event_type = event.get("e")
    if event_type == "outboundAccountPosition":
        return AccountPositionEvent(
            event_time_ms=int(event["E"]),
            update_time_ms=int(event["u"]),
            balances=[
                {"asset": item["a"], "free": Decimal(str(item["f"])), "locked": Decimal(str(item["l"]))}
                for item in event.get("B", [])
            ],
        )
    if event_type == "balanceUpdate":
        return BalanceUpdateEvent(
            event_time_ms=int(event["E"]),
            asset=str(event["a"]),
            delta=Decimal(str(event["d"])),
            clear_time_ms=int(event["T"]),
        )
    if event_type == "executionReport":
        return ExecutionReportEvent(
            event_time_ms=int(event["E"]),
            symbol=str(event["s"]),
            client_order_id=str(event["c"]),
            side=str(event["S"]),
            order_type=str(event["o"]),
            execution_type=str(event["x"]),
            order_status=str(event["X"]),
            reject_reason=str(event["r"]),
            order_id=int(event["i"]),
            last_executed_quantity=Decimal(str(event["l"])),
            cumulative_filled_quantity=Decimal(str(event["z"])),
            last_executed_price=Decimal(str(event["L"])),
            commission_amount=Decimal(str(event.get("n", "0"))),
            commission_asset=event.get("N"),
            transaction_time_ms=int(event["T"]),
        )
    if event_type == "listStatus":
        return ListStatusEvent(
            event_time_ms=int(event["E"]),
            symbol=str(event["s"]),
            order_list_id=int(event["g"]),
            list_status_type=str(event["l"]),
            list_order_status=str(event["L"]),
            reject_reason=str(event["r"]),
        )
    raise ValueError(f"unsupported user data event: {event_type}")


class UserDataStreamAdapter:
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.connected = False
        self.reconnect_count = 0
        self.last_message_ms: int | None = None
        self.listen_key = ""
        self.mode = "fallback-rest"

    def attach_listen_key(self, listen_key: str) -> None:
        self.listen_key = listen_key
        self.connected = bool(listen_key)
        self.mode = "connected" if listen_key else "fallback-rest"

    def mark_fallback(self) -> None:
        self.connected = False
        self.mode = "fallback-rest"

    def status(self) -> dict[str, object]:
        return {
            "profile": self.profile_name,
            "connected": self.connected,
            "reconnect_count": self.reconnect_count,
            "last_message_ms": self.last_message_ms,
            "mode": self.mode,
            "listen_key_present": bool(self.listen_key),
        }
