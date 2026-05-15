from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def build_milestone_evidence_graph(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    nodes = [
        {"id": "roadmap-100", "type": "roadmap", "path": "Roadmap docs/100-roadmap-end-to-end-paper-trading-operating-system-milestone-system-audit-production-readiness-simulation.md"},
        {"id": "system-inventory", "type": "report", "path": "data/milestone/system-inventory/system_inventory.json"},
        {"id": "safety-invariants", "type": "report", "path": "data/milestone/safety-invariants/system_safety_invariants.json"},
        {"id": "no-live-proof", "type": "proof", "path": "data/milestone/no-live/no_live_proof_pack.json"},
        {"id": "paper-simulation", "type": "paper_session", "path": "data/milestone/paper-os-simulation/paper_os_simulation.json"},
        {"id": "readiness-simulation", "type": "gate", "path": "data/milestone/readiness/production_readiness_simulation.json"},
    ]
    for node in nodes:
        node["exists"] = (root / node["path"]).exists()
    edges = [
        {"from": "roadmap-100", "to": "system-inventory", "relation": "requires"},
        {"from": "system-inventory", "to": "safety-invariants", "relation": "feeds"},
        {"from": "safety-invariants", "to": "no-live-proof", "relation": "proves_no_live"},
        {"from": "no-live-proof", "to": "readiness-simulation", "relation": "blocks_milestone"},
        {"from": "paper-simulation", "to": "readiness-simulation", "relation": "feeds"},
    ]
    missing = [node["id"] for node in nodes if not node["exists"]]
    return redact_payload(
        {
            "status": "ok" if not missing else "review",
            "nodes": nodes,
            "edges": edges,
            "missing_evidence": missing,
            "live_trading_enabled": False,
        }
    )


def write_milestone_evidence_graph(root: Path | str = ".", out_dir: Path | str | None = None) -> dict[str, str]:
    root = Path(root)
    out = Path(out_dir) if out_dir else root / "data" / "milestone" / "evidence-graph"
    out.mkdir(parents=True, exist_ok=True)
    payload = build_milestone_evidence_graph(root)
    json_path = out / "milestone_evidence_graph.json"
    md_path = out / "milestone_evidence_graph.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        f"# Milestone Evidence Graph\n\nStatus: {payload['status']}\nMissing evidence: {len(payload['missing_evidence'])}\nLive trading: disabled\n",
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}


def milestone_evidence_graph(nodes: int | None = None) -> dict[str, Any]:
    payload = build_milestone_evidence_graph(Path.cwd())
    if nodes is not None:
        payload["requested_nodes"] = nodes
    return payload
