from __future__ import annotations

from pathlib import Path
from typing import Any


REQUIRED_EVIDENCE = [
    "no_live_proof",
    "check_all",
    "unit_tests",
    "security_scan",
    "dashboard_smoke",
    "paper_simulation",
    "operator_quality_gate",
    "roadmap_traceability",
    "system_audit_report",
    "milestone_bundle_verify",
]


def detect_evidence_gaps(required: list[str], present: list[str]) -> dict[str, Any]:
    missing = sorted(set(required) - set(present))
    invalid: list[str] = []
    stale: list[str] = []
    priority = "P0" if "no_live_proof" in missing else "P1" if missing else "none"
    return {
        "status": "ok" if not missing and not invalid else "blocked" if priority == "P0" else "warn",
        "missing": missing,
        "invalid": invalid,
        "stale": stale,
        "recommended_commands": [f"python -m binance_spot_bot.cli {name.replace('_', '-')}" for name in missing],
        "priority": priority,
        "live_trading_enabled": False,
    }


def detect_evidence_gaps_in_dir(root: Path | str) -> dict[str, Any]:
    root = Path(root)
    present = []
    if (root / "data" / "milestone" / "no-live" / "no_live_proof_pack.json").exists():
        present.append("no_live_proof")
    if (root / "data" / "milestone" / "reports" / "system_audit_report.json").exists():
        present.append("system_audit_report")
    if (root / "data" / "milestone" / "paper-os-simulation" / "paper_os_simulation.json").exists():
        present.append("paper_simulation")
    if (root / "data" / "milestone" / "roadmap-traceability" / "roadmap_traceability_001_100.json").exists():
        present.append("roadmap_traceability")
    return detect_evidence_gaps(REQUIRED_EVIDENCE, present)


def evidence_gap_detector(required: list[str], present: list[str]) -> dict[str, Any]:
    return detect_evidence_gaps(required, present)
