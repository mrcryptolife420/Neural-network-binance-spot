from __future__ import annotations

from pathlib import Path
from typing import Any

from .portfolio_policy_registry import PolicyPromotionGateResult, PortfolioPolicyMetadata


def evaluate_policy_promotion(
    policy: PortfolioPolicyMetadata,
    *,
    operator_confirmed: bool,
    min_robustness: float = 0.6,
    max_drawdown: float = 25.0,
) -> PolicyPromotionGateResult:
    reasons: list[str] = []
    if not operator_confirmed:
        reasons.append("operator_confirmation_required")
    if policy.live_trading_enabled:
        reasons.append("live_trading_not_allowed")
    if policy.robustness_score < min_robustness:
        reasons.append("robustness_below_threshold")
    if float(policy.max_drawdown) > max_drawdown:
        reasons.append("drawdown_above_threshold")
    if not policy.policy_card_path:
        reasons.append("policy_card_missing")
    if not policy.evidence_manifest_path:
        reasons.append("evidence_manifest_missing")
    return PolicyPromotionGateResult(not reasons, reasons, policy.policy_id)


def evidence_paths_exist(policy: PortfolioPolicyMetadata, root: Path) -> dict[str, Any]:
    paths = {
        "policy_card": root / policy.policy_card_path if not Path(policy.policy_card_path).is_absolute() else Path(policy.policy_card_path),
        "evidence_manifest": root / policy.evidence_manifest_path if not Path(policy.evidence_manifest_path).is_absolute() else Path(policy.evidence_manifest_path),
    }
    missing = [name for name, path in paths.items() if not path.exists()]
    return {"status": "ok" if not missing else "warn", "missing": missing, "live_trading_enabled": False}
