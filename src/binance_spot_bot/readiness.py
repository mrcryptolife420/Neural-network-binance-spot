from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ReadinessScore:
    level: str
    passed: list[str]
    blockers: list[str]
    live_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


REQUIRED_EVIDENCE = ("check-all", "paper-report", "kill-switch-test", "secret-scan", "readiness-review")


def score_readiness(evidence_kinds: set[str]) -> ReadinessScore:
    passed = [kind for kind in REQUIRED_EVIDENCE if kind in evidence_kinds]
    blockers = [kind for kind in REQUIRED_EVIDENCE if kind not in evidence_kinds]
    level_index = min(len(passed), 5)
    return ReadinessScore(f"R{level_index}", passed, blockers, live_allowed=False)
