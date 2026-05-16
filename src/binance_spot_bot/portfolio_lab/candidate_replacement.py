from __future__ import annotations

from dataclasses import replace
from typing import Any

from .candidate_basket import PortfolioCandidateBasket, build_report


def simulate_candidate_replacements(basket: PortfolioCandidateBasket, decay_report: dict[str, Any], *, policy: str = "manual_review_required") -> dict[str, Any]:
    events = []
    items = list(basket.items)
    if policy == "manual_review_required":
        return {"status": "blocked", "blockers": ["manual review required for candidate replacement research"], "events": [], "basket_after": build_report(basket), "live_trading_enabled": False}
    for row in decay_report.get("decay", []):
        if row.get("status") in {"degraded", "remove_candidate_research_only"}:
            events.append({"item_id": row["item_id"], "symbol": row["symbol"], "policy": policy, "paper_only": True, "live_trading_enabled": False})
            items = [replace(item, disabled=True, blocked_reason="decay_research") if item.item_id == row["item_id"] else item for item in items]
    basket_after = replace(basket, basket_id=f"{basket.basket_id}-replacement", items=items)
    return {"status": "ok", "events": events, "basket_after": build_report(basket_after), "live_trading_enabled": False}

