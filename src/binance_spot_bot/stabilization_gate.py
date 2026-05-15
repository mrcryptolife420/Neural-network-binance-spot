from __future__ import annotations

from typing import Any


def evaluate_stabilization_gate(
    backlog: dict[str, Any],
    *,
    waivers: list[str] | None = None,
    profile: str = "standard",
    no_live_proof_status: str = "ok",
    evidence_status: str = "ok",
    secret_status: str = "ok",
) -> dict[str, Any]:
    waivers = waivers or []
    open_items = [item for item in backlog.get("items", []) if item.get("status") not in {"validated", "closed"}]
    unwaived = [item for item in open_items if item.get("item_id") not in waivers]
    p0 = [item for item in unwaived if item.get("priority") == "P0"]
    p1 = [item for item in unwaived if item.get("priority") == "P1"]
    blockers = []
    if p0:
        blockers.append("open P0 stabilization items")
    if profile in {"standard", "deep"} and p1:
        blockers.append("open unwaived P1 stabilization items")
    if no_live_proof_status != "ok":
        blockers.append("no-live proof failed")
    if secret_status != "ok":
        blockers.append("secret verification failed")
    if evidence_status == "blocked":
        blockers.append("evidence gate blocked")
    return {
        "status": "pass" if not blockers else "blocked",
        "profile": profile,
        "blockers": blockers,
        "open_p0": len(p0),
        "open_p1": len(p1),
        "live_trading_enabled": False,
    }


def stabilization_gate(blockers: list[str], waivers: list[str]) -> dict[str, Any]:
    remaining = sorted(set(blockers) - set(waivers))
    return {"status": "ok" if not remaining else "blocked", "blockers": remaining, "live_trading_enabled": False}
