from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .watchlists import validate_symbols


WATCHLIST_PACKS: dict[str, tuple[str, ...]] = {
    "binance_spot_majors": ("BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"),
    "stablecoin_pairs": ("BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT"),
    "operator_demo_watchlist": ("BTCUSDT", "ETHUSDT"),
    "low_scope_smoke_watchlist": ("BTCUSDT",),
}


def watchlist_packs_payload() -> dict[str, Any]:
    rows = []
    for pack_id, symbols in sorted(WATCHLIST_PACKS.items()):
        unique = tuple(dict.fromkeys(symbols))
        invalid = validate_symbols(unique)
        rows.append({"pack_id": pack_id, "symbols": list(unique), "status": "ok" if not invalid else "blocked", "invalid_symbols": invalid})
    return redact_dashboard_payload({"status": "ok", "watchlist_packs": rows, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False})
