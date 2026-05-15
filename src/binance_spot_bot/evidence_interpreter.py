from __future__ import annotations

from typing import Any


def interpret_evidence(items: list[str]) -> dict[str, Any]:
    missing = [item for item in items if item.startswith("missing:")]
    blockers = [item for item in items if "P0" in item or "no-live failed" in item.lower()]
    return {
        "status": "blocked" if blockers else "warn" if missing or not items else "ok",
        "items": items,
        "blockers": blockers,
        "warnings": missing,
        "next_action": "fix blockers then rerun evidence export" if blockers else "collect missing evidence" if missing else "continue",
        "no_live_proof": "required",
        "live_trading_enabled": False,
    }


def evidence_interpreter(items: list[str]) -> dict[str, Any]:
    return interpret_evidence(items)
