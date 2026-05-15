from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .market_snapshot_cache import demo_market_snapshot
from .public_endpoint_policy import NO_FINANCIAL_ADVICE_STATEMENT, NO_LIVE_STATEMENT


def run_multi_symbol_paper_analytics(symbols: list[str] | tuple[str, ...], *, root: Path | str = ".", confirm: str = "") -> dict[str, Any]:
    if confirm not in {"", "RUN_PAPER_ANALYTICS_ONLY"}:
        return {"status": "blocked", "blockers": ["paper analytics confirm must be RUN_PAPER_ANALYTICS_ONLY"], "live_trading_enabled": False}
    rows = []
    for symbol in symbols:
        snapshot = demo_market_snapshot(symbol.upper())
        klines = snapshot["klines"]
        start = float(klines[0][4])
        end = float(klines[-1][4])
        pnl = round((end - start) * 0.01, 6)
        rows.append(
            {
                "symbol": symbol.upper(),
                "paper_only": True,
                "candle_count": len(klines),
                "signal_count": max(1, len(klines) // 10),
                "block_count": 0,
                "fill_count": 2,
                "paper_pnl": pnl,
                "max_drawdown": min(0, pnl / 2),
                "fees_estimate": "0.02",
                "model_used": "fixture-paper-baseline",
            }
        )
    payload = redact_payload({"status": "ok", "symbols": rows, "no_live_statement": NO_LIVE_STATEMENT, "no_financial_advice_statement": NO_FINANCIAL_ADVICE_STATEMENT, "live_trading_enabled": False})
    out = Path(root) / "data" / "market-intelligence" / "paper-analytics"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "multi-symbol-paper-analytics.json"
    md_path = out / "multi-symbol-paper-analytics.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(f"# Multi-Symbol Paper Analytics\n\nSymbols: {len(rows)}\n\n{NO_FINANCIAL_ADVICE_STATEMENT}\n", encoding="utf-8")
    payload["json"] = str(json_path)
    payload["markdown"] = str(md_path)
    return payload
