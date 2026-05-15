from __future__ import annotations

from typing import Any


def classify_stabilization_finding(finding: dict[str, Any] | str) -> dict[str, Any]:
    text = finding if isinstance(finding, str) else " ".join(str(finding.get(key, "")) for key in ("category", "title", "description", "source"))
    lowered = text.lower()
    if any(term in lowered for term in ("live", "signed", "secret", "api key", "account endpoint", "order endpoint")):
        domain, priority = "safety_no_live", "P0"
    elif "check-all" in lowered or "safety" in lowered:
        domain, priority = "check_all", "P1"
    elif "dashboard" in lowered or "browser" in lowered:
        domain, priority = "dashboard_browser_smoke", "P1"
    elif "paper" in lowered or "simulation" in lowered:
        domain, priority = "runtime_paper_simulation", "P1"
    elif "slow" in lowered or "timeout" in lowered:
        domain, priority = "performance_slow", "P2"
    elif "flaky" in lowered:
        domain, priority = "flaky_check", "P2"
    elif "doc" in lowered or "runbook" in lowered:
        domain, priority = "docs_runbooks", "P3"
    else:
        domain, priority = "operator_evidence", "P2"
    return {
        "domain": domain,
        "priority": priority,
        "recommended_gate": "deep_milestone" if priority in {"P0", "P1"} else "standard_milestone",
        "auto_waivable": priority != "P0",
        "explanation": f"{domain} mapped to {priority}",
        "live_trading_enabled": False,
    }


def stabilization_classifier(item: str) -> dict[str, Any]:
    classified = classify_stabilization_finding(item)
    classified["class"] = "blocker" if classified["priority"] in {"P0", "P1"} else "task"
    return classified
