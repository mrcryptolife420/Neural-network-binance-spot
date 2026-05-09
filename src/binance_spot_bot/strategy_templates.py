from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class StrategyTemplate:
    key: str
    label: str
    mode: str
    parameters: dict[str, Any]
    auto_apply: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


TEMPLATES = (
    StrategyTemplate("no-trade", "No trade", "demo", {"signal": "HOLD"}),
    StrategyTemplate("buy-hold", "Buy hold research", "paper", {"rebalance": "manual", "max_entries": 1}),
    StrategyTemplate("momentum", "Momentum", "paper", {"ret_window_min": 0.002, "min_confidence": 0.65}),
    StrategyTemplate("mean-reversion", "Mean reversion", "paper", {"zscore_entry": 2.0, "min_confidence": 0.65}),
    StrategyTemplate("confidence-threshold", "Confidence threshold", "paper", {"min_confidence": 0.75}),
)


def list_strategy_templates() -> list[dict[str, Any]]:
    return [template.to_dict() for template in TEMPLATES]


def strategy_template(key: str) -> StrategyTemplate:
    for template in TEMPLATES:
        if template.key == key:
            return template
    raise ValueError(f"unsupported strategy template: {key}")
