from __future__ import annotations

from pathlib import Path
from typing import Any

from . import WALK_FORWARD_CONFIRM
from .allocation_decay import analyze_allocation_decay
from .allocation_proposals import propose_allocation
from .basket_simulation import simulate_basket
from .candidate_basket import PortfolioCandidateBasket, fixture_basket
from .common import json_write, stable_hash
from .dataset_coverage_audit import audit_dataset_coverage
from .rebalance_event_simulator import simulate_rebalance_events
from .rebalancing_schedules import default_rebalancing_schedules
from .walk_forward_splits import build_walk_forward_split


def preview_rolling_portfolio_simulation(basket: PortfolioCandidateBasket | None = None, allocation: dict[str, Any] | None = None) -> dict[str, Any]:
    basket = basket or fixture_basket()
    allocation = allocation or propose_allocation(basket)["proposal"]
    split = build_walk_forward_split(symbols=[item.symbol for item in basket.items])
    schedules = default_rebalancing_schedules()
    return {"status": "ok", "basket_id": basket.basket_id, "allocation_id": allocation.get("allocation_id"), "split": split, "schedules": schedules, "requires_confirm": WALK_FORWARD_CONFIRM, "live_trading_enabled": False}


def run_rolling_portfolio_simulation(root: Path, *, basket: PortfolioCandidateBasket | None = None, allocation: dict[str, Any] | None = None, confirm: str = "") -> dict[str, Any]:
    if confirm != WALK_FORWARD_CONFIRM:
        return {"status": "blocked", "blockers": [f"rolling simulation requires confirm {WALK_FORWARD_CONFIRM}"], "live_trading_enabled": False}
    basket = basket or fixture_basket()
    allocation = allocation or propose_allocation(basket)["proposal"]
    split = build_walk_forward_split(symbols=[item.symbol for item in basket.items])
    windows = split["split"]["windows"]
    schedules = default_rebalancing_schedules()["schedules"][:2]
    results = []
    for window in windows:
        for schedule in schedules:
            simulation = simulate_basket(basket, allocation, periods=24)
            events = simulate_rebalance_events(allocation, schedule, steps=24)
            results.append(
                {
                    "window_id": window["window_id"],
                    "schedule_id": schedule["schedule_id"],
                    "validation_paper_pnl": simulation["paper_pnl"],
                    "max_drawdown": simulation["max_drawdown"],
                    "turnover": simulation["turnover_estimate"] + sum(event["estimated_turnover"] for event in events["events"]),
                    "fees": simulation["fees_estimate"] + sum(event["estimated_fees"] for event in events["events"]),
                    "rebalance_events": events["events"],
                    "status": "ok",
                    "live_trading_enabled": False,
                }
            )
    report = {
        "status": "completed",
        "run_id": f"rolling-{stable_hash({'basket': basket.basket_id, 'allocation': allocation.get('allocation_id')})[:12]}",
        "split": split,
        "coverage": audit_dataset_coverage(split),
        "decay": analyze_allocation_decay(basket),
        "results": results,
        "live_trading_enabled": False,
    }
    report["saved"] = json_write(root / "data" / "portfolio-lab" / "walk-forward" / "runs" / f"{report['run_id']}.json", report)
    return report

