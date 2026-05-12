from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class RiskFactor:
    name: str
    weight: int
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def score_regression_risk(changed: list[str]) -> dict[str, Any]:
    factors: list[RiskFactor] = []
    for path in changed:
        lower = path.lower()
        if any(token in lower for token in ["live", "signed", "order", "account", "credential", "security", "redaction", "restore", "migration", "action_executor"]):
            factors.append(RiskFactor("critical_safety_surface", 90, path))
        elif any(token in lower for token in ["runtime", "execution", "risk", "cli.py"]):
            factors.append(RiskFactor("high_core_surface", 70, path))
        elif any(token in lower for token in ["ui/", "dashboard", "streamlit"]):
            factors.append(RiskFactor("dashboard_surface", 50, path))
        elif any(token in lower for token in ["docs/", "roadmap docs"]):
            factors.append(RiskFactor("docs_only", 20, path))
        else:
            factors.append(RiskFactor("general_change", 40, path))
    score = max([factor.weight for factor in factors], default=0)
    level = "critical" if score >= 85 else "high" if score >= 65 else "medium" if score >= 40 else "low"
    profile = "deep" if level in {"critical", "high"} else "standard" if level == "medium" else "fast"
    return {"status": "ready", "payload": {"score": score, "level": level, "profile": profile, "factors": [factor.to_dict() for factor in factors]}, "live_trading_enabled": False}


def regression_risk(changed: list[str]) -> dict[str, Any]:
    return score_regression_risk(changed)
