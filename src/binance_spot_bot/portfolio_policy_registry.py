from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload

ALLOWED_POLICY_STATUSES = {"candidate", "challenger", "champion", "suspended", "archived"}
FORBIDDEN_POLICY_STATUSES = {"live", "live_candidate", "live_champion", "production"}


@dataclass(frozen=True)
class PortfolioPolicyMetadata:
    policy_id: str
    policy_name: str
    policy_type: str
    alloc_weights: dict[str, str]
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
    prev_champion_id: str = ""
    governance_notes: str = ""
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    promoted_at_ms: int = 0
    live_trading_enabled: bool = False

    @property
    def previous_champion_id(self) -> str:
        return self.prev_champion_id

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class PolicyPromotionGateResult:
    allowed: bool
    reasons: list[str]
    policy_id: str
    required_evidence: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PolicyLineageRecord:
    policy_id: str
    parent_policy_id: str = ""
    prev_champion_id: str = ""
    action: str = "registered"
    reason: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PolicyGovernanceDecision:
    policy_id: str
    decision: str
    reasons: list[str]
    operator_confirmed: bool
    prev_champion_id: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False


class PortfolioPolicyRegistry:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "registry.json"

    def register(self, metadata: PortfolioPolicyMetadata) -> PortfolioPolicyMetadata:
        self._validate(metadata)
        payload = self._load()
        policies = {row["policy_id"]: row for row in payload.get("policies", [])}
        is_new = metadata.policy_id not in policies
        policies[metadata.policy_id] = metadata.to_dict()
        payload["policies"] = sorted(policies.values(), key=lambda row: row["policy_id"])
        if is_new:
            self._append_lineage(
                payload,
                PolicyLineageRecord(
                    policy_id=metadata.policy_id,
                    action="registered",
                    reason="policy_registered",
                    evidence_refs=[metadata.policy_card_path, metadata.evidence_manifest_path],
                ),
            )
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
        champion_id = self._load().get("latest_champion_id", "")
        if champion_id:
            try:
                return self.get(champion_id)
            except KeyError:
                return None
        champions = [policy for policy in self.list() if policy.status == "champion"]
        return champions[-1] if champions else None

    def lineage(self) -> list[dict[str, Any]]:
        return list(self._load().get("lineage", []))

    def decisions(self) -> list[dict[str, Any]]:
        return list(self._load().get("decisions", []))

    def set_champion(
        self,
        policy_id: str,
        *,
        operator_confirmed: bool,
        evidence_refs: list[str] | None = None,
    ) -> PolicyGovernanceDecision:
        current = self.champion()
        target = self.get(policy_id)
        if not operator_confirmed:
            decision = PolicyGovernanceDecision(
                policy_id=policy_id,
                decision="blocked",
                reasons=["operator_confirmation_required"],
                operator_confirmed=False,
                prev_champion_id=current.policy_id if current else "",
                evidence_refs=evidence_refs or [],
            )
            self._record_decision(decision)
            return decision
        payload = self._load()
        rows: list[dict[str, Any]] = []
        promoted_at = int(time.time() * 1000)
        for row in payload.get("policies", []):
            if row["policy_id"] == policy_id:
                row = {
                    **row,
                    "status": "champion",
                    "role": "champion",
                    "prev_champion_id": current.policy_id if current and current.policy_id != policy_id else row.get("prev_champion_id", ""),
                    "promoted_at_ms": promoted_at,
                    "live_trading_enabled": False,
                }
            elif row.get("status") == "champion":
                row = {**row, "status": "archived", "role": "prev_champion", "live_trading_enabled": False}
            rows.append(row)
        payload["policies"] = rows
        payload["latest_champion_id"] = policy_id
        self._append_lineage(
            payload,
            PolicyLineageRecord(
                policy_id=policy_id,
                prev_champion_id=current.policy_id if current else "",
                action="promoted",
                reason="operator_confirmed",
                evidence_refs=evidence_refs or [],
            ),
        )
        decision = PolicyGovernanceDecision(
            policy_id=target.policy_id,
            decision="promoted",
            reasons=["operator_confirmed", "paper_only"],
            operator_confirmed=True,
            prev_champion_id=current.policy_id if current else "",
            evidence_refs=evidence_refs or [],
        )
        payload.setdefault("decisions", []).append(asdict(decision))
        self._save(payload)
        return decision

    def update_status(self, policy_id: str, status: str, reason: str) -> PortfolioPolicyMetadata:
        if status in FORBIDDEN_POLICY_STATUSES or status not in ALLOWED_POLICY_STATUSES:
            raise ValueError("invalid paper policy status")
        payload = self._load()
        rows: list[dict[str, Any]] = []
        changed: PortfolioPolicyMetadata | None = None
        for row in payload.get("policies", []):
            if row["policy_id"] == policy_id:
                row = {**row, "status": status, "role": status, "governance_notes": reason, "live_trading_enabled": False}
                changed = PortfolioPolicyMetadata(**row)
                self._append_lineage(payload, PolicyLineageRecord(policy_id=policy_id, action=status, reason=reason))
            rows.append(row)
        if changed is None:
            raise KeyError(policy_id)
        if payload.get("latest_champion_id") == policy_id and status != "champion":
            payload["latest_champion_id"] = ""
        payload["policies"] = rows
        self._save(payload)
        return changed

    def suspend(self, policy_id: str, reason: str) -> PortfolioPolicyMetadata:
        return self.update_status(policy_id, "suspended", reason)

    def archive(self, policy_id: str, reason: str) -> PortfolioPolicyMetadata:
        return self.update_status(policy_id, "archived", reason)

    def _record_decision(self, decision: PolicyGovernanceDecision) -> None:
        payload = self._load()
        payload.setdefault("decisions", []).append(asdict(decision))
        self._save(payload)

    def _append_lineage(self, payload: dict[str, Any], record: PolicyLineageRecord) -> None:
        payload.setdefault("lineage", []).append(asdict(record))

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {
                "policies": [],
                "lineage": [],
                "decisions": [],
                "latest_champion_id": "",
                "live_trading_enabled": False,
            }
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, payload: dict[str, Any]) -> None:
        safe = redact_payload({**payload, "live_trading_enabled": False})
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
        tmp.replace(self.path)

    def _validate(self, metadata: PortfolioPolicyMetadata) -> None:
        if metadata.status in FORBIDDEN_POLICY_STATUSES or metadata.status not in ALLOWED_POLICY_STATUSES:
            raise ValueError("invalid paper policy status")
        if metadata.live_trading_enabled:
            raise ValueError("portfolio policy cannot enable live trading")
        if not metadata.policy_id.strip():
            raise ValueError("policy_id is required")


def demo_policy(policy_id: str = "policy-demo") -> PortfolioPolicyMetadata:
    return PortfolioPolicyMetadata(
        policy_id=policy_id,
        policy_name="Demo paper policy",
        policy_type="paper_portfolio",
        alloc_weights={"BTCUSDT": "0.50", "ETHUSDT": "0.50"},
        risk_budget_hash="risk-demo",
        scenario_weight_hash="scenario-demo",
        optimizer_id="optimizer-demo",
        benchmark_id="benchmark-demo",
        robustness_score=0.74,
        max_drawdown="5.0",
        worst_case_scenario="volatile",
        policy_card_path="docs/portfolio-policy-registry.md",
        evidence_manifest_path="docs/roadmap-082-122-correctie-audit-2026-05-11.md",
        status="candidate",
        role="candidate",
        live_trading_enabled=False,
    )
