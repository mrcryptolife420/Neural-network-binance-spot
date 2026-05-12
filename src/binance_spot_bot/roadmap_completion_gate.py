from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_EVIDENCE = ["tests_passed", "check_all_passed", "no_live_proof"]


def evaluate_roadmap_completion_gate(
    roadmap: int | str,
    *,
    evidence: dict[str, Any] | None = None,
    dashboard_touched: bool = False,
) -> dict[str, Any]:
    evidence = evidence or {}
    blockers = [name for name in REQUIRED_EVIDENCE if not evidence.get(name)]
    if dashboard_touched and not evidence.get("browser_smoke_passed"):
        blockers.append("browser_smoke_required")
    if dashboard_touched and not evidence.get("dashboard_smoke_passed"):
        blockers.append("dashboard_smoke_required")
    status = "ready_to_complete" if not blockers else ("needs_tests" if "tests_passed" in blockers else "needs_evidence")
    return {
        "status": status,
        "roadmap": f"{int(str(roadmap).lstrip('0') or '0'):03d}" if str(roadmap).isdigit() else str(roadmap),
        "blockers": blockers,
        "evidence": evidence,
        "live_trading_enabled": False,
    }


def write_completion_gate_report(payload: dict[str, Any], out: Path | str) -> dict[str, Any]:
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "roadmap_completion_gate.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    lines = ["# Roadmap Completion Gate", "", f"- Status: {payload['status']}"]
    lines.extend(f"- Blocker: {item}" for item in payload.get("blockers", []))
    lines.append("- Live trading enabled: false")
    (out_dir / "roadmap_completion_gate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {**payload, "paths": {"json": str(out_dir / "roadmap_completion_gate.json"), "markdown": str(out_dir / "roadmap_completion_gate.md")}}


def roadmap_completion_gate(tests_ok: bool, evidence_present: bool) -> dict[str, Any]:
    payload = evaluate_roadmap_completion_gate(
        "000",
        evidence={"tests_passed": tests_ok, "check_all_passed": tests_ok, "no_live_proof": evidence_present},
    )
    if payload["status"] == "ready_to_complete":
        payload["status"] = "ok"
    return payload
