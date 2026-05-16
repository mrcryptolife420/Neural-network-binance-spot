from __future__ import annotations

from typing import Any


VALID_TRANSITIONS = {
    "draft": {"dataset_ready"},
    "dataset_ready": {"validation_running"},
    "validation_running": {"validation_passed", "blocked"},
    "validation_passed": {"paper_replay_required"},
    "paper_replay_required": {"paper_replay_passed"},
    "paper_replay_passed": {"testnet_required"},
    "testnet_required": {"testnet_passed"},
    "testnet_passed": {"live_readiness_candidate"},
}


def create_model_candidate(dataset: dict[str, Any]) -> dict[str, Any]:
    return {"status": "ok", "candidate": {"candidate_id": "model-candidate-fixture", "model_alias": "tiny_nn_v1", "strategy_id": "rule_baseline", "dataset_version": dataset.get("manifest", {}).get("dataset_id"), "promotion_state": "dataset_ready", "blockers": [], "live_trading_enabled": False}, "live_trading_enabled": False}


def validate_candidate_transition(from_state: str, to_state: str) -> dict[str, Any]:
    ok = to_state in VALID_TRANSITIONS.get(from_state, set())
    return {"status": "ok" if ok else "blocked", "from_state": from_state, "to_state": to_state, "live_trading_enabled": False}

