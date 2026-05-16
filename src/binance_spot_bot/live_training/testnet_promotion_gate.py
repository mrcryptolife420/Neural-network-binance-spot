from __future__ import annotations

from typing import Any


def evaluate_testnet_promotion_gate(target_report: dict[str, Any], quality_v2: dict[str, Any], validation: dict[str, Any], paper_replay: dict[str, Any]) -> dict[str, Any]:
    blockers = []
    if target_report.get("status") == "blocked":
        blockers.append("collect more demo data")
    if quality_v2.get("grade") not in {"A", "B"}:
        blockers.append("fix dataset quality")
    if validation.get("grade") not in {"A", "B"}:
        blockers.append("validation required")
    if paper_replay.get("status") != "ok":
        blockers.append("paper replay required")
    state = "ready_for_testnet_rehearsal" if not blockers else "not_ready"
    return {"status": "ok" if not blockers else "blocked", "state": state, "blockers": blockers, "max_testnet_order_size_quote": 25.0, "live_trading_enabled": False}

