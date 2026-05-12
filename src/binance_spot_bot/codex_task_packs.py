from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


FORBIDDEN_FILES = [".env", "*.pem", "data/secrets/*", "live_trading/*"]
SAFETY_CONSTRAINTS = [
    "local-only roadmap execution",
    "live_trading_enabled must remain false",
    "no signed Binance endpoints",
    "no order or account endpoints",
    "no API keys in files, logs, reports, or task packs",
]


@dataclass(frozen=True)
class CodexFileBoundary:
    allowed_files: list[str]
    forbidden_files: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CodexTask:
    task_id: str
    title: str
    goal: str
    phase: str
    file_boundary: CodexFileBoundary
    required_tests: list[str]
    required_docs: list[str]
    required_evidence: list[str]
    safety_constraints: list[str]
    validation_commands: list[str]
    acceptance_criteria: list[str]
    rollback_notes: str

    def to_dict(self) -> dict[str, Any]:
        return {**asdict(self), "live_trading_enabled": False}


@dataclass(frozen=True)
class CodexTaskPack:
    task_pack_id: str
    roadmap_number: int
    roadmap_title: str
    tasks: list[CodexTask]
    no_live_statement: str = "Live trading blijft disabled; geen signed/order/account endpoints."

    def to_dict(self) -> dict[str, Any]:
        return {**asdict(self), "live_trading_enabled": False}


def codex_task_pack(roadmap: str) -> dict[str, Any]:
    task = CodexTask(
        task_id="pr-01",
        title=f"Implement {roadmap} foundation",
        goal="Build the smallest production implementation with tests and evidence.",
        phase="foundation",
        file_boundary=CodexFileBoundary(["src/binance_spot_bot/*", "tests/*", "docs/*"], FORBIDDEN_FILES),
        required_tests=["python -m pytest -q"],
        required_docs=["docs/"],
        required_evidence=["data/roadmaps/evidence/"],
        safety_constraints=SAFETY_CONSTRAINTS,
        validation_commands=["python -m binance_spot_bot.cli check-all --skip-tests --json"],
        acceptance_criteria=["tests pass", "evidence exists", "no-live proof present"],
        rollback_notes="Revert scoped files only; do not touch user data or secrets.",
    )
    pack = CodexTaskPack("manual-task-pack", 0, roadmap, [task])
    return {"status": "ready", "task_pack": pack.to_dict(), "live_trading_enabled": False}


def validate_task_pack_no_live(pack: dict[str, Any]) -> dict[str, Any]:
    raw = str(pack).lower()
    blockers = []
    if "live_trading_enabled': true" in raw or '"live_trading_enabled": true' in raw:
        blockers.append("live_enabled")
    for forbidden in ["signed endpoint", "place order", "account endpoint"]:
        if forbidden in raw and "no " not in raw:
            blockers.append(forbidden.replace(" ", "_"))
    return {"status": "blocked" if blockers else "ok", "blockers": blockers, "live_trading_enabled": False}
