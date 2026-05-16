from __future__ import annotations

from typing import Any


def evaluate_split_governance(dataset: dict[str, Any]) -> dict[str, Any]:
    features = dataset.get("manifest", {}).get("features", [])
    blockers = []
    if len(features) < 3:
        blockers.append("too few samples for split")
    if dataset.get("manifest", {}).get("leakage_report", {}).get("status") != "ok":
        blockers.append("leakage report failed")
    return {"status": "blocked" if blockers else "ok", "splits": {"train": 0.6, "validation": 0.2, "test": 0.2}, "blockers": blockers, "test_split_tuning_allowed": False, "live_trading_enabled": False}

