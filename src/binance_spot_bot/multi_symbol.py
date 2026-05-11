from __future__ import annotations

import json
import re
import time
from decimal import Decimal
from pathlib import Path
from typing import Iterable

from .redaction import redact_payload

DEFAULT_DEMO_SYMBOLS = ("BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "LINKUSDT")


def normalize_symbol(value: str) -> str:
    symbol = re.sub(r"[^A-Za-z0-9]", "", value).upper()
    if not symbol:
        return ""
    if not symbol.endswith("USDT") and len(symbol) <= 6:
        symbol = f"{symbol}USDT"
    return symbol


def parse_symbol_list(value: str | Iterable[str], *, max_symbols: int = 12) -> list[str]:
    if isinstance(value, str):
        tokens = re.split(r"[\s,;]+", value)
    else:
        tokens = list(value)
    symbols: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        symbol = normalize_symbol(str(token))
        if len(symbol) < 6 or symbol in seen:
            continue
        seen.add(symbol)
        symbols.append(symbol)
        if len(symbols) >= max_symbols:
            break
    return symbols


def choose_active_symbols(selected: Iterable[str], custom: str, *, max_active: int) -> list[str]:
    requested = [*parse_symbol_list(selected, max_symbols=50), *parse_symbol_list(custom, max_symbols=50)]
    return parse_symbol_list(requested, max_symbols=max(1, max_active))


def validate_demo_symbols(symbols: Iterable[str], *, max_active: int = 10) -> dict[str, object]:
    valid_symbols = parse_symbol_list(symbols, max_symbols=max_active)
    blockers: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    if not valid_symbols:
        blockers.append({"name": "symbols.empty", "message": "Select at least one symbol"})
    if len(valid_symbols) > max_active:
        blockers.append({"name": "symbols.too_many", "message": f"Use at most {max_active} symbols"})
    for symbol in valid_symbols:
        if not symbol.isalnum():
            blockers.append({"name": "symbols.invalid_chars", "message": f"{symbol} contains invalid characters"})
        if not symbol.endswith("USDT"):
            warnings.append({"name": "symbols.quote_asset", "message": f"{symbol} is not a USDT quote pair"})
    return {
        "status": "fail" if blockers else "warn" if warnings else "ok",
        "valid_symbols": valid_symbols,
        "blockers": blockers,
        "warnings": warnings,
        "live_trading_enabled": False,
    }


def allocation_plan(
    symbols: Iterable[str],
    *,
    total_quote_budget: Decimal,
    default_quote_size: Decimal,
    max_position_quote: Decimal,
) -> list[dict[str, str]]:
    active = parse_symbol_list(symbols, max_symbols=50)
    if not active:
        return []
    per_symbol = total_quote_budget / Decimal(len(active))
    rows: list[dict[str, str]] = []
    for symbol in active:
        budget = min(per_symbol, max_position_quote)
        rows.append(
            {
                "symbol": symbol,
                "quote_budget": str(budget.quantize(Decimal("0.01"))),
                "default_order_quote": str(default_quote_size),
                "max_position_quote": str(max_position_quote),
                "status": "warn" if default_quote_size > budget else "ok",
            }
        )
    return rows


def risk_limit_rows(
    symbols: Iterable[str],
    *,
    max_open_orders_per_symbol: int,
    max_trades: int,
    max_position_quote: Decimal,
    max_daily_loss: Decimal,
    max_spread: Decimal,
    min_conf: float,
) -> list[dict[str, object]]:
    return [
        {
            "symbol": symbol,
            "max_open_orders": max_open_orders_per_symbol,
            "max_trades": max_trades,
            "max_position_quote": str(max_position_quote),
            "max_daily_loss_quote": str(max_daily_loss),
            "max_spread_bps": str(max_spread),
            "min_signal_confidence": min_conf,
            "live_trading_enabled": False,
        }
        for symbol in parse_symbol_list(symbols, max_symbols=50)
    ]


def summarize_multi_rows(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    items = list(rows)
    by_status: dict[str, int] = {}
    total_fills = 0
    total_open_orders = 0
    total_equity = Decimal("0")
    for row in items:
        status = str(row.get("status", "unknown"))
        by_status[status] = by_status.get(status, 0) + 1
        total_fills += int(row.get("fills", 0) or 0)
        total_open_orders += int(row.get("open_orders", 0) or 0)
        try:
            total_equity += Decimal(str(row.get("equity", "0")))
        except Exception:
            pass
    return {
        "active_bots": by_status.get("running", 0),
        "symbols": len(items),
        "total_fills": total_fills,
        "total_open_orders": total_open_orders,
        "total_equity": str(total_equity),
        "by_status": by_status,
        "live_trading_enabled": False,
    }


def next_multi_action(
    *,
    has_keys: bool,
    connection_status: str,
    armed: bool,
    validation_status: str,
    running: bool,
) -> str:
    if not has_keys:
        return "Enter demo keys"
    if connection_status == "not-tested":
        return "Test demo connection"
    if validation_status == "fail":
        return "Fix selected symbols"
    if not armed:
        return "Connect demo trading"
    if running:
        return "Watch multi-symbol bots or stop selected symbols"
    return "Start selected symbols"


def write_multi_symbol_evidence(
    data_dir: Path,
    *,
    symbols: list[str],
    rows: list[dict[str, object]],
    validation: dict[str, object],
    allocation: list[dict[str, str]],
    summary: dict[str, object],
) -> dict[str, object]:
    path = data_dir / "evidence" / "multi-symbol" / "multi-symbol-demo-evidence.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = redact_payload(
        {
            "created_at_ms": int(time.time() * 1000),
            "symbols": symbols,
            "validation": validation,
            "allocation": allocation,
            "rows": rows,
            "summary": summary,
            "live_trading_enabled": False,
        }
    )
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return {"status": "ok", "path": str(path), "live_trading_enabled": False}
