from __future__ import annotations

from pathlib import Path
from typing import Any


ARTIFACT_ROOTS = ["data/checks", "data/evidence", "data/reports", "data/support", "data/sessions", "data/pilot-runs", "data/roadmaps", "data/releases", "data/metrics", "data/backups", "data/action-center", "data/compliance"]


def build_artifact_flow_graph(root: Path | str = ".") -> dict[str, Any]:
    root_path = Path(root)
    nodes = []
    edges = []
    for artifact_root in ARTIFACT_ROOTS:
        path = root_path / artifact_root
        nodes.append({"id": artifact_root, "type": "data_directory", "exists": path.exists()})
        if "support" in artifact_root:
            edges.append({"source": "support-bundle", "target": artifact_root, "type": "writes"})
        if "checks" in artifact_root:
            edges.append({"source": "check-all", "target": artifact_root, "type": "writes"})
        if "roadmaps" in artifact_root:
            edges.append({"source": "roadmap-evidence-export", "target": artifact_root, "type": "writes"})
    return {"status": "ready", "nodes": nodes, "edges": edges, "missing_producers": [], "live_trading_enabled": False}


def artifact_flow_graph(artifacts: list[str]) -> dict[str, Any]:
    return {"status": "ready", "nodes": artifacts, "edges": [], "live_trading_enabled": False}
