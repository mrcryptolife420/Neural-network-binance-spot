from __future__ import annotations

from pathlib import Path
from typing import Any

from .dev_quality_facade import evidence_bundle, write_dev_report
from .local_paper_os_facade import safe_record


def training_payload(name: str, rows: int = 0) -> dict[str, Any]:
    return safe_record(name, {"rows": rows, "feature_contract": "local-paper-v1"})


def drift_score(current: list[float], baseline: list[float]) -> dict[str, Any]:
    avg_current = sum(current) / len(current) if current else 0.0
    avg_base = sum(baseline) / len(baseline) if baseline else 0.0
    score = abs(avg_current - avg_base)
    return safe_record("drift_score", {"score": round(score, 6), "status": "warn" if score > 0.2 else "ok"})


def ensemble_vote(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    if not predictions:
        return safe_record("ensemble_prediction", {"signal": "HOLD", "confidence": 0.0})
    confidence = sum(float(row.get("confidence", 0)) for row in predictions) / len(predictions)
    buys = sum(1 for row in predictions if row.get("signal") == "BUY")
    signal = "BUY" if buys > len(predictions) / 2 else "HOLD"
    return safe_record("ensemble_prediction", {"signal": signal, "confidence": round(confidence, 4)})


def system_audit() -> dict[str, Any]:
    return safe_record("system_audit", {"invariants": ["no_live", "kill_switch", "paper_only"], "status": "ready"})


def stabilization_status(blockers: list[str]) -> dict[str, Any]:
    return safe_record("stabilization", {"blockers": blockers, "status": "ok" if not blockers else "blocked"})


def operator_training_payload(topic: str) -> dict[str, Any]:
    return safe_record("operator_training", {"topic": topic, "required_score": 80})


def write_model_ops_report(root: Path, name: str, payload: dict[str, Any]) -> dict[str, str]:
    return write_dev_report(root, name, payload)


def export_model_ops_evidence(files: list[Path], out: Path) -> dict[str, Any]:
    return evidence_bundle(files, out)
