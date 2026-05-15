from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .local_paper_os_facade import safe_record
from .no_live_proof_pack import build_no_live_proof_pack
from .roadmap_milestone_traceability import build_roadmap_milestone_traceability
from .system_inventory import system_inventory
from .system_safety_invariants import audit_system_safety_invariants


def build_paper_os_simulation(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    inventory = system_inventory(root)
    invariants = audit_system_safety_invariants(root)
    proof = build_no_live_proof_pack(root)
    traceability = build_roadmap_milestone_traceability(root)
    blockers = []
    if invariants["status"] != "ok":
        blockers.extend(invariants["hard_failures"])
    if proof["status"] != "ok":
        blockers.append("no-live proof blocked")
    payload = {
        "status": "ready" if not blockers else "blocked",
        "profile": "standard_milestone",
        "inventory_status": inventory["status"],
        "subsystems": len(inventory["subsystems"]),
        "invariants": [item["name"] for item in invariants["invariants"]],
        "no_live_proof_status": proof["status"],
        "roadmap_traceability_status": traceability["status"],
        "paper_session": {"steps": 3, "fills": 0, "risk_blocks_expected": True},
        "blockers": blockers,
        "live_trading_enabled": False,
        "signed_endpoints_used": False,
        "account_endpoints_required": False,
    }
    return safe_record("paper_os_simulation", payload, status=payload["status"])


def write_paper_os_simulation(root: Path | str = ".", out_dir: Path | str | None = None) -> dict[str, str]:
    root = Path(root)
    out = Path(out_dir) if out_dir else root / "data" / "milestone" / "paper-os-simulation"
    out.mkdir(parents=True, exist_ok=True)
    payload = build_paper_os_simulation(root)
    json_path = out / "paper_os_simulation.json"
    md_path = out / "paper_os_simulation.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        f"# Paper OS Simulation\n\nStatus: {payload['payload']['status']}\nLive trading: disabled\nSigned endpoints used: False\n",
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}


def paper_os_simulation() -> dict[str, Any]:
    return build_paper_os_simulation(Path.cwd())
