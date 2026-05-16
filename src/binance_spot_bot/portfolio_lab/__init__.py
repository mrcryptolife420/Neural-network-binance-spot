from __future__ import annotations

from typing import Any

NO_LIVE_STATEMENT = "PORTFOLIO LAB - PAPER ONLY - NO LIVE TRADING"
NO_ADVICE_STATEMENT = "Portfolio Lab output is local paper research, not financial advice."
PAPER_ONLY_RESEARCH_STATEMENT = "Portfolio Lab simulations are paper-only research and never create real allocations."
PAPER_PORTFOLIO_CONFIRM = "RUN_PAPER_PORTFOLIO_RESEARCH_ONLY"
WALK_FORWARD_CONFIRM = "RUN_WALK_FORWARD_PAPER_RESEARCH_ONLY"


def portfolio_lab_health() -> dict[str, Any]:
    return {
        "status": "ok",
        "paper_only": True,
        "local_only": True,
        "public_or_fixture_data_only": True,
        "requires_api_keys": False,
        "live_trading_enabled": False,
        "signed_endpoints_enabled": False,
        "account_endpoints_enabled": False,
        "order_endpoints_enabled": False,
        "no_live_statement": NO_LIVE_STATEMENT,
        "no_financial_advice_statement": NO_ADVICE_STATEMENT,
        "paper_only_research_statement": PAPER_ONLY_RESEARCH_STATEMENT,
    }


def assert_portfolio_lab_safe(payload: dict[str, Any] | None = None) -> None:
    if payload and payload.get("live_trading_enabled") is True:
        raise ValueError("portfolio lab refuses live trading")
