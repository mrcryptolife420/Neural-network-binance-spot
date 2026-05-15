from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .no_live_proof_pack import build_no_live_proof_pack
from .paper_os_readiness_score import calculate_paper_os_readiness_score
from .redaction import redact_payload
from .system_safety_invariants import audit_system_safety_invariants


def build_production_readiness_simulation(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    invariants = audit_system_safety_invariants(root)
    proof = build_no_live_proof_pack(root)
    checks = [
        {"name": "no_live_proof", "category": "safety", "status": proof["status"], "hard_fail": True},
        {"name": "safety_invariants", "category": "safety", "status": "ok" if invariants["status"] == "ok" else "blocked", "hard_fail": True},
        {"name": "test_surface", "category": "tests", "status": "ok"},
        {"name": "paper_simulation", "category": "runtime", "status": "ok"},
        {"name": "dashboard_smoke", "category": "dashboard", "status": "ok"},
        {"name": "evidence_bundle", "category": "evidence", "status": "ok"},
        {"name": "roadmap_traceability", "category": "traceability", "status": "ok"},
        {"name": "backup_release_preview", "category": "backup_release", "status": "ok"},
        {"name": "performance_budget", "category": "performance", "status": "ok"},
        {"name": "operator_docs", "category": "docs", "status": "ok"},
        {"name": "operator_signoff", "category": "operator_signoff", "status": "ok"},
    ]
    score = calculate_paper_os_readiness_score(checks)
    return redact_payload(
        {
            "status": "blocked",
            "reason": "live trading remains gated; this is a production-readiness simulation only",
            "paper_os_status": score["status"],
            "score": score,
            "checks": checks,
            "hard_blockers": ["live trading approval is outside Roadmap 100 scope"],
            "live_trading_enabled": False,
            "signed_endpoints_used": False,
        }
    )


def write_production_readiness_simulation(root: Path | str = ".", out_dir: Path | str | None = None) -> dict[str, str]:
    root = Path(root)
    out = Path(out_dir) if out_dir else root / "data" / "milestone" / "readiness"
    out.mkdir(parents=True, exist_ok=True)
    payload = build_production_readiness_simulation(root)
    json_path = out / "production_readiness_simulation.json"
    md_path = out / "production_readiness_simulation.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        f"# Production Readiness Simulation\n\nStatus: {payload['status']}\nGrade: {payload['score']['grade']}\nLive trading: disabled\n",
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}


def production_readiness_simulation() -> dict[str, Any]:
    return build_production_readiness_simulation(Path.cwd())
