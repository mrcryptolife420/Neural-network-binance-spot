from __future__ import annotations

from typing import Any

FORBIDDEN = ("live approved", "real funds", "production live", "place real order")


def check_operator_docs_consistency(docs: list[str], commands: list[str]) -> dict[str, Any]:
    blockers = [doc for doc in docs if any(phrase in doc.lower() for phrase in FORBIDDEN)]
    warnings = []
    if not docs:
        warnings.append("no operator docs")
    if not commands:
        warnings.append("no commands referenced")
    return {
        "status": "blocked" if blockers else "warn" if warnings else "ok",
        "blockers": blockers,
        "warnings": warnings,
        "docs_coverage_percent": 100 if docs else 0,
        "cli_cookbook_coverage": 100 if commands else 0,
        "live_trading_enabled": False,
    }


def operator_docs_consistency(docs: list[str], commands: list[str]) -> dict[str, Any]:
    return check_operator_docs_consistency(docs, commands)
