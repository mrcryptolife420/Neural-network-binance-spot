from __future__ import annotations

from decimal import Decimal
from typing import Any

from binance_spot_bot.redaction import redact_payload
from . import NO_ADVICE_STATEMENT, NO_LIVE_STATEMENT


def _dec(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def compare_strategy_results(results: list[dict[str, Any]], *, sort_by: str = "paper_pnl") -> dict[str, Any]:
    rows = []
    for row in results:
        pnl = _dec(row.get("paper_pnl"))
        drawdown = abs(_dec(row.get("max_drawdown")))
        ratio = pnl / (drawdown or Decimal("1"))
        fills = _dec(row.get("fill_count"))
        blocks = _dec(row.get("block_count"))
        rows.append(
            {
                "job_id": row.get("job_id"),
                "symbol": row.get("symbol"),
                "strategy_id": row.get("strategy_id"),
                "model_alias": row.get("model_alias"),
                "risk_preset": row.get("risk_preset"),
                "paper_pnl": str(pnl),
                "max_drawdown": str(row.get("max_drawdown", "0")),
                "return_drawdown_ratio": str(ratio.quantize(Decimal("0.0001"))),
                "fill_rate": str((fills / max(Decimal("1"), _dec(row.get("signal_count")))).quantize(Decimal("0.0001"))),
                "block_rate": str((blocks / max(Decimal("1"), fills + blocks)).quantize(Decimal("0.0001"))),
                "stability_score": max(0, 100 - int(drawdown * 10)),
            }
        )
    rows.sort(key=lambda item: _dec(item.get(sort_by, 0)), reverse=True)
    return redact_payload({"status": "ok", "rows": rows, "no_live_statement": NO_LIVE_STATEMENT, "no_advice_statement": NO_ADVICE_STATEMENT, "live_trading_enabled": False})
