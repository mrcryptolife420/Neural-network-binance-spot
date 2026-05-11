from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .redaction import redact_payload

FORBIDDEN_TERMS = {
    "place order",
    "place an order",
    "market buy",
    "market sell",
    "cancel order",
    "enable live",
    "live trading",
    "toon mijn api",
    "show my api",
    "secret",
    "credential",
    "verborgen",
    "withdraw",
    "disable kill",
    "bypass risk",
    "upload",
}


@dataclass(frozen=True)
class AiOpsIntent:
    intent: str
    confidence: float
    reason: str
    forbidden: bool = False
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def classify_ai_ops_query(question: str) -> dict[str, Any]:
    normalized = question.lower()
    if any(term in normalized for term in FORBIDDEN_TERMS):
        return AiOpsIntent("forbidden_action", 0.99, "forbidden trading/secret/live intent", True).to_dict()
    mapping = [
        ("health_summary", ["health", "gezondheid", "status", "lager"]),
        ("explain_anomaly", ["anomaly", "anomalie", "waarom", "failed", "faalde"]),
        ("failed_jobs", ["job", "scheduled", "faalden", "failed jobs"]),
        ("report_freshness", ["report", "rapport", "fresh", "stale"]),
        ("evidence_missing", ["evidence", "ontbreekt", "missing"]),
        ("support_bundle_summary", ["support bundle", "bundle"]),
        ("runbook_recommendation", ["runbook", "volgen"]),
        ("command_suggestion", ["command", "voorstel", "maak"]),
        ("governance_status", ["governance", "policy", "beleid"]),
        ("data_growth_explanation", ["data growth", "budget", "cache"]),
        ("dashboard_error_help", ["dashboard", "smoke", "traceback"]),
        ("check_all_explanation", ["check-all", "check all"]),
    ]
    for intent, terms in mapping:
        if any(term in normalized for term in terms):
            return AiOpsIntent(intent, 0.82, f"matched keywords for {intent}").to_dict()
    return AiOpsIntent("unknown_safe_question", 0.35, "no strong local intent match").to_dict()
