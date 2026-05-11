from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload, redact_text


@dataclass(frozen=True)
class OperatorDecision:
    decision_id: str
    proposal_id: str
    operator_id_local: str
    decision: str
    reason_text: str = ""
    reason_codes: list[str] = field(default_factory=list)
    evidence_links: list[str] = field(default_factory=list)
    risk_acknowledgement: str = ""
    confirm_phrase_used: str = ""
    previous_status: str = ""
    next_status: str = ""
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    redacted: bool = True
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {
            **asdict(self),
            "reason_text": redact_text(self.reason_text),
            "confirm_phrase_used": "[CONFIRMED]" if self.confirm_phrase_used else "",
            "redacted": True,
            "live_trading_enabled": False,
        }
        payload["decision_hash"] = stable_decision_hash(payload)
        return redact_payload(payload)


@dataclass(frozen=True)
class DecisionJournalExport:
    path: str
    markdown_path: str
    count: int
    manifest_hash: str
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class DecisionJournal:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "decision-journal.jsonl"

    def append(self, decision: OperatorDecision) -> OperatorDecision:
        payload = decision.to_dict()
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=str) + "\n")
        (self.root / "latest-decision.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return decision

    def entries(self, *, limit: int = 500, since_ms: int | None = None) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if since_ms is not None:
            rows = [row for row in rows if int(row.get("created_at_ms", 0)) >= since_ms]
        return rows[-limit:]

    def export(self, *, days: int = 7) -> DecisionJournalExport:
        since = int(time.time() * 1000) - max(1, days) * 86_400_000
        rows = self.entries(since_ms=since)
        out = self.root / f"decision-journal-{days}d.json"
        md = self.root / f"decision-journal-{days}d.md"
        payload = {"entries": rows, "count": len(rows), "live_trading_enabled": False}
        manifest_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
        payload["manifest_hash"] = manifest_hash
        out.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
        md.write_text(_journal_markdown(rows, manifest_hash), encoding="utf-8")
        return DecisionJournalExport(str(out), str(md), len(rows), manifest_hash)


def append_decision(root: Path, decision: dict) -> dict[str, Any]:
    journal = DecisionJournal(root / "action-center")
    payload = OperatorDecision(
        decision_id=str(decision.get("decision_id") or f"dec-{int(time.time() * 1000)}"),
        proposal_id=str(decision.get("proposal_id", "")),
        operator_id_local=str(decision.get("operator_id_local", "local-operator")),
        decision=str(decision.get("decision", "defer")),
        reason_text=str(decision.get("reason_text", decision.get("reason", ""))),
        reason_codes=list(decision.get("reason_codes", [])),
        evidence_links=list(decision.get("evidence_links", [])),
        risk_acknowledgement=str(decision.get("risk_acknowledgement", "")),
        confirm_phrase_used=str(decision.get("confirm_phrase_used", "")),
        previous_status=str(decision.get("previous_status", "")),
        next_status=str(decision.get("next_status", "")),
    )
    journal.append(payload)
    return {"status": "ok", "decision": payload.to_dict(), "path": str(journal.path), "live_trading_enabled": False}


def stable_decision_hash(payload: dict[str, Any]) -> str:
    clean = {key: value for key, value in payload.items() if key != "decision_hash"}
    return hashlib.sha256(json.dumps(redact_payload(clean), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]


def _journal_markdown(rows: list[dict[str, Any]], manifest_hash: str) -> str:
    lines = ["# Operator Decision Journal", "", f"Manifest hash: `{manifest_hash}`", "", "| Time | Proposal | Decision | Next status |", "|---|---|---|---|"]
    for row in rows:
        lines.append(f"| {row.get('created_at_ms')} | {row.get('proposal_id')} | {row.get('decision')} | {row.get('next_status')} |")
    lines.append("")
    lines.append("Live trading enabled: false")
    return "\n".join(lines)
