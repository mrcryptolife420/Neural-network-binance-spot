from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload

ALLOWED_POLICY_STATUSES = {"candidate", "challenger", "champion", "suspended", "archived"}


@dataclass(frozen=True)
class PortfolioPolicyMetadata:
    policy_id: str
    policy_name: str
    policy_type: str
    allocation_weights: dict[str, str]
    risk_budget_hash: str
    scenario_weight_hash: str
    optimizer_id: str
    benchmark_id: str
    robustness_score: float
    max_drawdown: str
    worst_case_scenario: str
    policy_card_path: str
    evidence_manifest_path: str
    status: str = "candidate"
    role: str = "candidate"
    previous_champion_id: str = ""
    governance_notes: str = ""
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    promoted_at_ms: int = 0
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class PolicyPromotionGateResult:
    allowed: bool
    reasons: list[str]
    policy_id: str
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PolicyLineageRecord:
    policy_id: str
    parent_policy_id: str
    previous_champion_id: str
    decision: str
    reason: str
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PolicyGovernanceDecision:
    policy_id: str
    decision: str
    reasons: list[str]
    operator_confirmed: bool
    live_trading_enabled: bool = False


class PortfolioPolicyRegistry:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "registry.json"

    def register(self, metadata: PortfolioPolicyMetadata) -> PortfolioPolicyMetadata:
        self._validate(metadata)
        payload = self._load()
        policies = {row["policy_id"]: row for row in payload.get("policies", [])}
        policies[metadata.policy_id] = metadata.to_dict()
        payload["policies"] = list(policies.values())
        self._save(payload)
        return metadata

    def list(self) -> list[PortfolioPolicyMetadata]:
        return [PortfolioPolicyMetadata(**row) for row in self._load().get("policies", [])]

    def get(self, policy_id: str) -> PortfolioPolicyMetadata:
        for policy in self.list():
            if policy.policy_id == policy_id:
                return policy
        raise KeyError(policy_id)

    def champion(self) -> PortfolioPolicyMetadata | None:
        champions = [policy for policy in self.list() if policy.status == "champion"]
        return champions[-1] if champions else None

    def set_champion(self, policy_id: str, *, operator_confirmed: bool) -> PolicyGovernanceDecision:
        current = self.champion()
        target = self.get(policy_id)
        if not operator_confirmed:
            return PolicyGovernanceDecision(policy_id, "blocked", ["operator_confirmation_required"], False)
        payload = self._load()
        rows = []
        for row in payload.get("policies", []):
            if row["policy_id"] == policy_id:
                row = {**row, "status": "champion", "role": "champion", "previous_champion_id": current.policy_id if current else "", "promoted_at_ms": int(time.time() * 1000)}
            elif row.get("status") == "champion":
                row = {**row, "status": "archived", "role": "previous_champion"}
            rows.append(row)
        payload["policies"] = rows
        payload.setdefault("lineage", []).append(
            asdict(PolicyLineageRecord(policy_id, "", current.policy_id if current else "", "promote", "operator_confirmed"))
        )
        self._save(payload)
        return PolicyGovernanceDecision(target.policy_id, "promoted", ["operator_confirmed"], True)

    def update_status(self, policy_id: str, status: str, reason: str) -> PortfolioPolicyMetadata:
        if status not in ALLOWED_POLICY_STATUSES:
            raise ValueError("invalid paper policy status")
        payload = self._load()
        changed = None
        rows = []
        for row in payload.get("policies", []):
            if row["policy_id"] == policy_id:
                row = {**row, "status": status, "role": status, "governance_notes": reason}
                changed = PortfolioPolicyMetadata(**row)
            rows.append(row)
        if changed is None:
            raise KeyError(policy_id)
        payload["policies"] = rows
        self._save(payload)
        return changed

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"policies": [], "lineage": [], "live_trading_enabled": False}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, payload: dict[str, Any]) -> None:
        safe = redact_payload({**payload, "live_trading_enabled": False})
        self.path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")

    def _validate(self, metadata: PortfolioPolicyMetadata) -> None:
        if metadata.status not in ALLOWED_POLICY_STATUSES:
            raise ValueError("invalid paper policy status")
        if metadata.live_trading_enabled:
            raise ValueError("portfolio policy cannot enable live trading")


def demo_policy(policy_id: str = "policy-demo") -> PortfolioPolicyMetadata:
    return PortfolioPolicyMetadata(
        policy_id=policy_id,
        policy_name="Demo paper policy",
        policy_type="paper_portfolio",
        allocation_weights={"BTCUSDT": "0.50", "ETHUSDT": "0.50"},
        risk_budget_hash="risk-demo",
        scenario_weight_hash="scenario-demo",
        optimizer_id="optimizer-demo",
        benchmark_id="benchmark-demo",
        robustness_score=0.74,
        max_drawdown="5.0",
        worst_case_scenario="volatile",
        policy_card_path="data/paper-portfolio/policies/policy-card.md",
        evidence_manifest_path="data/evidence/manifest/evidence-chain.json",
    )
