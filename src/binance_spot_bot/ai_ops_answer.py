from __future__ import annotations

from pathlib import Path
from typing import Any

from .ai_ops_command_proposals import propose_ai_ops_command
from .ai_ops_context import build_ai_ops_context
from .ai_ops_query import classify_ai_ops_query
from .ai_ops_runbook_recommender import recommend_runbook
from .redaction import redact_payload


def answer_ai_ops_query(question: str, *, root: Path | None = None, context: dict[str, Any] | None = None) -> dict[str, Any]:
    intent = classify_ai_ops_query(question)
    if intent["forbidden"]:
        return redact_payload(
            {
                "status": "blocked",
                "summary": "Ik kan geen live trading, orders, accountacties, secrets of externe uploads uitvoeren of voorstellen.",
                "answer": "Blocked: read-only AI Ops Assistant.",
                "intent": intent,
                "evidence": [],
                "recommended_next_safe_action": "run redaction-self-test or open the relevant local runbook",
                "command_proposal": None,
                "confidence": intent["confidence"],
                "missing_context": [],
                "sources": [],
                "safety_note": "AI OPS ASSISTANT - READ ONLY. Live trading remains disabled.",
                "live_trading_enabled": False,
            }
        )
    ctx = context or build_ai_ops_context(root or Path("data"))
    sources = [source["name"] for source in ctx.get("context", {}).get("manifest", {}).get("sources", [])]
    missing = list(ctx.get("context", {}).get("manifest", {}).get("warnings", []))
    runbook = recommend_runbook(question)
    command = _command_for_intent(intent["intent"])
    proposal = propose_ai_ops_command(command, reason=f"intent:{intent['intent']}") if command else None
    summary = _summary_for_intent(intent["intent"], sources, missing)
    return redact_payload(
        {
            "status": "answered",
            "summary": summary,
            "answer": summary,
            "intent": intent,
            "evidence": sources[:5],
            "root_cause_hypothesis": "Based on local redacted artifacts only; inspect listed sources for exact details.",
            "recommended_next_safe_action": runbook["runbook"],
            "recommended_runbook": runbook,
            "command_proposal": proposal,
            "confidence": intent["confidence"],
            "missing_context": missing,
            "sources": sources,
            "safety_note": "AI OPS ASSISTANT - READ ONLY. Command proposals are not executed.",
            "live_trading_enabled": False,
        }
    )


def _command_for_intent(intent: str) -> str:
    return {
        "health_summary": "operator-health-score --json",
        "explain_anomaly": "metrics-anomalies --json",
        "failed_jobs": "local-job-list --json",
        "report_freshness": "report-index --json",
        "evidence_missing": "evidence-manifest --json",
        "support_bundle_summary": "support-bundles-verify --json",
        "runbook_recommendation": "runbook-list --json",
        "command_suggestion": "diagnostics --json",
        "governance_status": "governance-reminders --json",
        "data_growth_explanation": "data-growth-budget --json",
        "dashboard_error_help": "dashboard-smoke --seconds 1",
        "check_all_explanation": "check-all --skip-tests --json",
    }.get(intent, "")


def _summary_for_intent(intent: str, sources: list[str], missing: list[str]) -> str:
    if not sources:
        return "Ik heb onvoldoende lokale context om dit zeker te beantwoorden. Bouw eerst een AI Ops context pack."
    base = f"Lokale context bevat {len(sources)} bron(nen). Intent: {intent}."
    if missing:
        base += f" Ontbrekende context: {', '.join(missing[:3])}."
    return base
