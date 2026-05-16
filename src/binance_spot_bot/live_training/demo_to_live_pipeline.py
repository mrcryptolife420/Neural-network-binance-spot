from __future__ import annotations

from pathlib import Path
from typing import Any

from .dataset_quality_burndown import build_dataset_quality_burndown
from .demo_dataset_quality_v2 import evaluate_demo_dataset_quality_v2
from .demo_dataset_vault import ingest_demo_vault
from .demo_session_targets import calculate_demo_session_target_progress, default_demo_session_target, fixture_complete_sessions
from .demo_spot_data_recorder import record_demo_spot_events
from .demo_to_live_evidence import export_demo_to_live_evidence
from .feature_label_dataset import build_feature_label_dataset_v2
from .live_candidate_gate import evaluate_live_candidate_gate
from .model_candidate_registry import create_model_candidate
from .model_strategy_validation import run_model_strategy_validation
from .paper_replay_from_demo import run_paper_replay_from_demo
from .split_governance import evaluate_split_governance
from .testnet_promotion_gate import evaluate_testnet_promotion_gate
from .testnet_rehearsal_runner import TESTNET_REHEARSAL_CONFIRM, run_testnet_rehearsal


def run_demo_to_live_pipeline(root: Path, *, testnet_confirm: str = TESTNET_REHEARSAL_CONFIRM) -> dict[str, Any]:
    recording = record_demo_spot_events(root)
    target = calculate_demo_session_target_progress(default_demo_session_target(), fixture_complete_sessions())
    vault = ingest_demo_vault(root, [recording])
    burndown = build_dataset_quality_burndown(vault, target)
    quality = evaluate_demo_dataset_quality_v2(vault, target, burndown)
    dataset = build_feature_label_dataset_v2(root, vault, quality)
    split = evaluate_split_governance(dataset)
    candidate = create_model_candidate(dataset)
    validation = run_model_strategy_validation(candidate, quality, split)
    replay = run_paper_replay_from_demo(dataset, validation)
    promotion = evaluate_testnet_promotion_gate(target, quality, validation, replay)
    rehearsal = run_testnet_rehearsal(promotion, confirm=testnet_confirm)
    evidence = export_demo_to_live_evidence(root, {"run_id": "demo-to-live-pipeline", "target": target, "quality": quality, "validation": validation, "promotion": promotion, "rehearsal": rehearsal, "live_trading_enabled": False})
    live_candidate = evaluate_live_candidate_gate(evidence, rehearsal)
    return {
        "status": "ok",
        "recording": recording,
        "target": target,
        "vault": vault,
        "burndown": burndown,
        "quality": quality,
        "dataset": dataset,
        "split": split,
        "candidate": candidate,
        "validation": validation,
        "paper_replay": replay,
        "testnet_promotion": promotion,
        "testnet_rehearsal": rehearsal,
        "live_candidate": live_candidate,
        "evidence": evidence,
        "live_trading_enabled": False,
    }

