from __future__ import annotations

from pathlib import Path
from typing import Any

from .roadmap_index import build_roadmap_index_object


def build_roadmap_traceability(root: Path | str = ".") -> dict[str, Any]:
    idx = build_roadmap_index_object(root)
    edges = []
    missing = []
    for roadmap in idx.roadmaps:
        rid = f"roadmap:{roadmap.number:03d}" if roadmap.number else roadmap.path
        for module in roadmap.parse.linked_modules:
            edges.append({"source": rid, "target": module, "type": "introduces_or_modifies"})
        for test in roadmap.parse.linked_tests:
            edges.append({"source": test, "target": rid, "type": "validates"})
        if not roadmap.parse.linked_modules and roadmap.location == "voltooid_docs":
            missing.append(roadmap.path)
    return {"status": "ready", "edges": edges, "missing_traceability": missing, "live_trading_enabled": False}


def roadmap_traceability(roadmap: str, files: list[str]) -> dict[str, Any]:
    return {"status": "ready", "roadmap": roadmap, "files": files, "live_trading_enabled": False}
