from __future__ import annotations

from itertools import product
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .experiment_queue import build_queue_from_candidates


PRESET_LIMITS = {
    "small_safe_smoke": {"max_symbols": 2, "intervals": ("1m",), "strategies": ("momentum_research",), "models": ("rule_based",), "risks": ("conservative",)},
    "scanner_top10_paper": {"max_symbols": 10, "intervals": ("1m", "5m"), "strategies": ("momentum_research",), "models": ("rule_based", "demo-model"), "risks": ("conservative", "balanced")},
    "model_compare": {"max_symbols": 5, "intervals": ("1m",), "strategies": ("momentum_research",), "models": ("rule_based", "demo-model", "candidate"), "risks": ("conservative",)},
    "risk_compare": {"max_symbols": 5, "intervals": ("1m",), "strategies": ("momentum_research",), "models": ("rule_based",), "risks": ("conservative", "balanced", "research_aggressive")},
}


def expand_experiment_matrix(candidates: list[dict[str, Any]], *, preset: str = "small_safe_smoke", max_jobs: int = 50) -> dict[str, Any]:
    cfg = PRESET_LIMITS.get(preset, PRESET_LIMITS["small_safe_smoke"])
    base = candidates[: int(cfg["max_symbols"])]
    expanded: list[dict[str, Any]] = []
    for candidate, interval, strategy, model, risk in product(base, cfg["intervals"], cfg["strategies"], cfg["models"], cfg["risks"]):
        item = dict(candidate)
        item["interval"] = interval
        item["strategy_id"] = strategy
        item["model_alias"] = model
        item["risk_preset"] = risk
        expanded.append(item)
        if len(expanded) >= max_jobs:
            break
    queue = build_queue_from_candidates(expanded, preset=preset, name=f"{preset} queue")
    return redact_payload({"status": "ok", "preset": preset, "expanded_jobs": len(expanded), "queue": queue, "live_trading_enabled": False})
