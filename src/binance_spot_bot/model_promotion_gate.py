from __future__ import annotations

from typing import Any


def model_promotion_gate(
    score: float,
    operator_confirmed: bool,
    *,
    leakage_pass: bool = True,
    feature_contract_ok: bool = True,
    inference_compatible: bool = True,
    latency_ok: bool = True,
    model_card_present: bool = True,
    beats_baseline: bool | None = None,
) -> dict[str, Any]:
    checks = {
        "score_threshold": score >= 0.6,
        "operator_confirmed": operator_confirmed,
        "leakage_pass": leakage_pass,
        "feature_contract_ok": feature_contract_ok,
        "inference_compatible": inference_compatible,
        "latency_ok": latency_ok,
        "model_card_present": model_card_present,
        "beats_baseline": score >= 0.6 if beats_baseline is None else beats_baseline,
    }
    blockers = [name for name, ok in checks.items() if not ok]
    return {
        "status": "ok" if not blockers else "blocked",
        "scope": "paper_shadow_demo_only",
        "checks": checks,
        "blockers": blockers,
        "live_trading_enabled": False,
    }
