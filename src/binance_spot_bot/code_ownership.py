from __future__ import annotations

from typing import Any


DOMAINS = {
    "runtime": ["runtime", "pilot", "session"],
    "execution": ["execution", "order"],
    "risk": ["risk", "kill"],
    "data": ["data", "dataset", "feature", "indicator"],
    "dashboard": ["ui/", "dashboard", "streamlit"],
    "operator_ops": ["operator", "support", "evidence"],
    "security_redaction": ["security", "redaction", "credentials"],
    "roadmap_execution": ["roadmap", "codex_task", "pr_template"],
    "release_management": ["release", "migration", "upgrade", "rollback"],
    "disaster_recovery": ["backup", "restore", "disaster"],
    "permissions_compliance": ["permission", "compliance", "role"],
    "ai_ops": ["ai_ops", "ops_assistant"],
    "portfolio": ["portfolio", "allocation", "ensemble"],
    "tests": ["tests/"],
    "docs": ["docs/"],
}


def owner_for_file(path: str) -> str:
    lower = path.lower().replace("\\", "/")
    if any(token in lower for token in DOMAINS["security_redaction"]):
        return "security_redaction"
    for domain, tokens in DOMAINS.items():
        if any(token in lower for token in tokens):
            return domain
    return "unknown"


def build_code_ownership(files: list[str]) -> dict[str, Any]:
    items = [{"path": path, "owner": owner_for_file(path), "safety_level": "critical" if owner_for_file(path) in {"security_redaction", "execution", "risk", "release_management"} else "normal"} for path in files]
    unknown = [item["path"] for item in items if item["owner"] == "unknown"]
    return {"status": "ready", "payload": {"files": items, "unknown": unknown, "domains": sorted(DOMAINS)}, "live_trading_enabled": False}


def code_ownership(files: list[str]) -> dict[str, Any]:
    return build_code_ownership(files)
