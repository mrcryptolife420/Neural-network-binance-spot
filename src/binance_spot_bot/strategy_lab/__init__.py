from __future__ import annotations

NO_LIVE_STATEMENT = "STRATEGY LAB - PAPER ONLY - NO LIVE TRADING"
NO_ADVICE_STATEMENT = "STRATEGY LAB OUTPUT IS RESEARCH ONLY AND NOT FINANCIAL ADVICE"
PAPER_ONLY_CONFIRM = "RUN_PAPER_EXPERIMENTS_ONLY"

FORBIDDEN_ENDPOINTS = (
    "place_order",
    "cancel_order",
    "test_order",
    "get_account_state",
    "open_orders",
    "query_order",
)


def strategy_lab_health() -> dict[str, object]:
    return {
        "status": "ok",
        "paper_only": True,
        "requires_api_keys": False,
        "no_live_statement": NO_LIVE_STATEMENT,
        "no_advice_statement": NO_ADVICE_STATEMENT,
        "live_trading_enabled": False,
    }


def assert_strategy_lab_safe(payload: dict[str, object] | None = None) -> None:
    text = str(payload or {}).lower()
    if "live" in text and "no live" not in text and "live_trading_enabled': false" not in text and '"live_trading_enabled": false' not in text:
        raise ValueError("strategy lab payload may not enable live trading")
    if any(endpoint in text for endpoint in FORBIDDEN_ENDPOINTS):
        raise ValueError("strategy lab payload references forbidden endpoint")
