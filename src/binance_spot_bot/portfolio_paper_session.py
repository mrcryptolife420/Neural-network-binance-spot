from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
import json
from pathlib import Path
from typing import Any

from .portfolio import Portfolio
from .portfolio_risk import PortfolioRiskEngine


@dataclass(frozen=True)
class PortfolioPaperResult:
    status: str
    portfolio: dict[str, Any]
    blocks: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_portfolio_paper_session(symbols: list[str], initial_quote: Decimal, marks: dict[str, Decimal], risk: PortfolioRiskEngine) -> PortfolioPaperResult:
    portfolio = Portfolio()
    portfolio.set_balance("USDT", initial_quote)
    blocks = []
    for symbol in symbols:
        allowed, reason = risk.can_enter(portfolio, symbol, marks)
        if not allowed:
            blocks.append(f"{symbol}: {reason}")
            continue
        portfolio.buy(symbol, "USDT", Decimal("10"), marks[symbol])
        risk.record_trade(symbol)
    return PortfolioPaperResult("completed", portfolio.to_dict(), blocks)


def export_portfolio_report(result: PortfolioPaperResult, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.to_dict(), indent=2, default=str), encoding="utf-8")
    return path
