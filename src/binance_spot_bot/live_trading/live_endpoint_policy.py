from __future__ import annotations

from typing import Any

from . import REAL_ORDER_CONFIRM

READ_ONLY_ENDPOINTS = {"server_time", "get_exchange_info", "get_symbol_filters", "get_klines", "get_order_book", "get_24hr_ticker", "get_book_ticker", "get_account_state"}
DRY_RUN_ENDPOINTS = READ_ONLY_ENDPOINTS | {"local_order_preview"}
PREVIEW_ENDPOINTS = DRY_RUN_ENDPOINTS | {"test_order"}
FIRST_ORDER_ENDPOINTS = PREVIEW_ENDPOINTS | {"place_order", "query_order"}


def endpoint_allowed(phase: str, endpoint: str, *, confirm: str = "") -> bool:
    if phase == "read_only":
        return endpoint in READ_ONLY_ENDPOINTS
    if phase == "dry_run":
        return endpoint in DRY_RUN_ENDPOINTS
    if phase == "preview":
        return endpoint in PREVIEW_ENDPOINTS and endpoint != "place_order"
    if phase == "first_order":
        if endpoint == "place_order" and confirm != REAL_ORDER_CONFIRM:
            return False
        return endpoint in FIRST_ORDER_ENDPOINTS
    return False


def live_endpoint_policy_report(phase: str, requested_endpoints: list[str] | None = None, *, confirm: str = "") -> dict[str, Any]:
    requested_endpoints = requested_endpoints or ["server_time", "get_account_state", "place_order"]
    decisions = {endpoint: endpoint_allowed(phase, endpoint, confirm=confirm) for endpoint in requested_endpoints}
    blockers = [f"endpoint blocked: {endpoint}" for endpoint, allowed in decisions.items() if not allowed]
    return {"status": "blocked" if blockers else "ok", "phase": phase, "decisions": decisions, "blockers": blockers, "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}
