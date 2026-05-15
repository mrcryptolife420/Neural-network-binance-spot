from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .public_endpoint_policy import NO_LIVE_STATEMENT


@dataclass(frozen=True)
class ScannerRateLimitBudget:
    max_symbols_per_scan: int = 50
    max_requests_per_scan: int = 160
    max_concurrency: int = 4
    min_scan_interval_seconds: int = 60
    cache_first: bool = True


def scanner_rate_limit_plan(symbols: list[str] | tuple[str, ...], endpoints: tuple[str, ...] = ("ticker", "book_ticker", "klines"), budget: ScannerRateLimitBudget | None = None) -> dict[str, Any]:
    budget = budget or ScannerRateLimitBudget()
    symbols = tuple(symbols)
    request_count = len(symbols) * len(endpoints)
    effective_requests = max(0, request_count - len(symbols)) if budget.cache_first else request_count
    blockers = []
    warnings = []
    if len(symbols) > budget.max_symbols_per_scan:
        blockers.append("symbol count exceeds budget")
    if effective_requests > budget.max_requests_per_scan:
        blockers.append("request count exceeds budget")
    if len(symbols) > 20:
        warnings.append("large scan should use cache-first mode")
    return redact_payload(
        {
            "status": "ok" if not blockers else "blocked",
            "budget": asdict(budget),
            "symbols": len(symbols),
            "endpoints": list(endpoints),
            "estimated_requests": effective_requests,
            "blockers": blockers,
            "warnings": warnings,
            "no_live_statement": NO_LIVE_STATEMENT,
            "live_trading_enabled": False,
        }
    )
