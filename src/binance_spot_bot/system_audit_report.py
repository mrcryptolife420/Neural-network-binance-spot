from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .no_live_proof_pack import build_no_live_proof_pack
from .paper_os_simulation import build_paper_os_simulation
from .production_readiness_simulation import build_production_readiness_simulation
from .redaction import redact_payload
from .system_inventory import system_inventory
from .system_safety_invariants import audit_system_safety_invariants


def build_system_audit_report(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    inventory = system_inventory(root)
    invariants = audit_system_safety_invariants(root)
    proof = build_no_live_proof_pack(root)
    simulation = build_paper_os_simulation(root)
    readiness = build_production_readiness_simulation(root)
    blockers = []
    blockers.extend(invariants.get("hard_failures", []))
    if proof["status"] != "ok":
        blockers.append("no-live proof failed")
    payload = {
        "status": "ready" if not blockers else "blocked",
        "executive_summary": "Paper OS milestone audit completed with live trading disabled.",
        "inventory": {"status": inventory["status"], "subsystems": len(inventory["subsystems"])},
        "safety_invariants": invariants,
        "no_live_proof": proof,
        "paper_simulation": {"status": simulation["payload"]["status"]},
        "production_readiness_simulation": readiness,
        "blockers": blockers,
        "warnings": invariants.get("warnings", []),
        "recommended_next_actions": ["continue Roadmap 101 stabilization before any live research"],
        "operator_signoff": "draft_required",
        "live_trading_enabled": False,
        "signed_endpoints_used": False,
    }
    return redact_payload(payload)


def write_system_audit_report(root: Path, payload: dict | None = None) -> dict[str, str]:
    payload = payload or build_system_audit_report(root)
    out = root / "data" / "milestone" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    safe = redact_payload(payload)
    json_path = out / "system_audit_report.json"
    md_path = out / "system_audit_report.md"
    json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# System Audit Report",
                "",
                f"Status: {safe['status']}",
                f"Subsystems: {safe['inventory']['subsystems']}",
                f"Readiness grade: {safe['production_readiness_simulation']['score']['grade']}",
                "Live trading: disabled",
                "Signed endpoints used: False",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
