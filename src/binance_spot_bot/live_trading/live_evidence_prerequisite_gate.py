from __future__ import annotations

from pathlib import Path
from typing import Any

from binance_spot_bot.portfolio_lab.common import json_write, redact_value, stable_hash, status_from_blockers

from . import NO_AUTO_LIVE_START_STATEMENT, NOT_FINANCIAL_ADVICE_STATEMENT


def fixture_live_evidence(*, quality_grade: str = "A", validation_grade: str = "A", testnet_ok: bool = True, live_candidate_review: bool = True) -> dict[str, Any]:
    rehearsal_status = "ok" if testnet_ok else "blocked"
    return {
        "demo_target": {"status": "ok"},
        "dataset_quality": {"status": "ok", "grade": quality_grade, "no_secret_proof": True},
        "model_validation": {"status": "ok" if validation_grade in {"A", "B"} else "blocked", "grade": validation_grade},
        "paper_replay": {"status": "ok"},
        "testnet_promotion": {"status": "ok", "state": "ready_for_testnet_rehearsal"},
        "testnet_rehearsal": {"status": rehearsal_status},
        "live_candidate": {"status": "review" if live_candidate_review else "blocked", "state": "live_readiness_review" if live_candidate_review else "live_execution_gate_required"},
        "manifest": {"hashes": ["fixture-hash"], "manifest_hash": "fixture-manifest"},
        "live_trading_enabled": False,
    }


def evaluate_live_evidence_prerequisites(evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    evidence = redact_value(evidence or {})
    blockers: list[str] = []
    warnings: list[str] = []
    if not evidence:
        blockers.append("Roadmap 117 evidence manifest missing")
    quality = evidence.get("dataset_quality", {})
    validation = evidence.get("model_validation", {})
    if quality.get("grade") not in {"A", "B"}:
        blockers.append("dataset quality grade below B")
    if validation.get("grade") not in {"A", "B"}:
        blockers.append("model validation grade below B")
    if evidence.get("paper_replay", {}).get("status") != "ok":
        blockers.append("paper replay missing or failed")
    if evidence.get("testnet_promotion", {}).get("status") != "ok":
        blockers.append("testnet promotion missing or failed")
    if evidence.get("testnet_rehearsal", {}).get("status") != "ok":
        blockers.append("testnet rehearsal missing or failed")
    live_candidate = evidence.get("live_candidate", {})
    if live_candidate.get("state") != "live_readiness_review":
        blockers.append("live candidate review not reached")
    text = str(evidence).lower()
    if "secret" in text and "[redacted]" not in text and "no_secret_proof" not in text:
        blockers.append("secret leak finding")
    if "live event contamination" in text:
        blockers.append("live contamination finding")
    if not evidence.get("manifest", {}).get("hashes"):
        blockers.append("evidence hashes missing")
    state = "eligible_for_live_dry_run" if not blockers else "blocked_missing_evidence"
    if any("quality" in item for item in blockers):
        state = "blocked_low_quality_data"
    elif any("validation" in item or "paper replay" in item for item in blockers):
        state = "blocked_validation_failed"
    elif any("testnet" in item for item in blockers):
        state = "blocked_testnet_failed"
    elif any("secret" in item for item in blockers):
        state = "blocked_secret_leak"
    return redact_value(
        {
            "status": status_from_blockers(blockers, warnings),
            "state": state,
            "evidence_hash": stable_hash(evidence) if evidence else "",
            "blockers": blockers,
            "warnings": warnings,
            "next_required_actions": blockers[:5],
            "no_auto_live_start_statement": NO_AUTO_LIVE_START_STATEMENT,
            "not_financial_advice_statement": NOT_FINANCIAL_ADVICE_STATEMENT,
            "live_execution_enabled": False,
            "live_order_placement_enabled": False,
            "live_trading_enabled": False,
        }
    )


def write_live_evidence_prerequisite_report(root: Path, report: dict[str, Any]) -> dict[str, Any]:
    return json_write(root / "data" / "live-trading" / "evidence-prerequisites" / "live_evidence_prerequisites.json", report)
