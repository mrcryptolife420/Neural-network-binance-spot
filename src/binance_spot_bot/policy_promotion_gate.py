from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .portfolio_policy_registry import PolicyPromotionGateResult, PortfolioPolicyMetadata

REQUIRED_PROMOTION_EVIDENCE = [
    "policy_card",
    "evidence_manifest",
    "benchmark_evidence",
    "robustness_evidence",
    "overfit_guard",
    "paper_approval",
    "no_live_proof",
]


def evaluate_policy_promotion(
    policy: PortfolioPolicyMetadata,
    operator_confirmed: bool,
    min_robustness: float = 0.6,
    max_drawdown: float = 25.0,
    evidence_payload: dict[str, Any] | None = None,
    root: Path | None = None,
) -> PolicyPromotionGateResult:
    reasons: list[str] = []
    evidence = evidence_payload or {}
    if not operator_confirmed:
        reasons.append("operator_confirmation_required")
    if policy.live_trading_enabled:
        reasons.append("live_trading_not_allowed")
    if policy.status in {"live", "live_candidate", "live_champion", "production"}:
        reasons.append("live_status_not_allowed")
    if policy.robustness_score < min_robustness:
        reasons.append("robustness_below_threshold")
    if _as_float(policy.max_drawdown) > max_drawdown:
        reasons.append("drawdown_above_threshold")
    if not policy.policy_card_path:
        reasons.append("policy_card_missing")
    if not policy.evidence_manifest_path:
        reasons.append("evidence_manifest_missing")

    if root is not None:
        path_status = evidence_paths_exist(policy, root)
        reasons.extend(path_status["missing"])
        evidence = {**_load_json_if_possible(root, policy.evidence_manifest_path), **evidence}

    required_flags = {
        "benchmark_evidence": evidence.get("benchmark_status") in {"pass", "ok", True},
        "robustness_evidence": float(evidence.get("robustness_score", policy.robustness_score)) >= min_robustness,
        "overfit_guard": evidence.get("overfit_guard") in {"pass", "ok", True},
        "paper_approval": evidence.get("paper_approval") in {"approved", "pass", True},
        "no_live_proof": evidence.get("live_trading_enabled", False) is False and evidence.get("signed_endpoint_used", False) is False,
    }
    for name, ok in required_flags.items():
        if not ok:
            reasons.append(f"{name}_missing_or_failed")

    return PolicyPromotionGateResult(
        allowed=not reasons,
        reasons=sorted(set(reasons)),
        policy_id=policy.policy_id,
        required_evidence=REQUIRED_PROMOTION_EVIDENCE,
        live_trading_enabled=False,
    )


def evidence_paths_exist(policy: PortfolioPolicyMetadata, root: Path) -> dict[str, Any]:
    paths = {
        "policy_card_missing": _resolve(root, policy.policy_card_path),
        "evidence_manifest_missing": _resolve(root, policy.evidence_manifest_path),
    }
    missing = [name for name, path in paths.items() if not path.exists()]
    return {"status": "ok" if not missing else "blocked", "missing": missing, "live_trading_enabled": False}


def _resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 999999.0


def _load_json_if_possible(root: Path, value: str) -> dict[str, Any]:
    path = _resolve(root, value)
    if not path.exists() or path.suffix.lower() != ".json":
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}
