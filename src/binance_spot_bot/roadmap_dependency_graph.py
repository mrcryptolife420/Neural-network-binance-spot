from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .roadmap_index import build_roadmap_index_object


def build_roadmap_dependency_graph(root: Path | str = ".", out: Path | str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    idx = build_roadmap_index_object(root_path)
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, str]] = []
    missing_tests: list[str] = []
    unlinked_docs: list[str] = []
    for roadmap in idx.roadmaps:
        rid = f"roadmap:{roadmap.number:03d}" if roadmap.number is not None else f"roadmap:{roadmap.path}"
        nodes[rid] = {"id": rid, "type": "roadmap", "label": roadmap.title, "path": roadmap.path}
        for previous in roadmap.parse.follows_on:
            edges.append({"source": f"roadmap:{previous:03d}", "target": rid, "type": "follows_on"})
        for module in roadmap.parse.linked_modules:
            mid = f"module:{module}"
            nodes[mid] = {"id": mid, "type": "module", "path": module}
            edges.append({"source": rid, "target": mid, "type": "implements"})
        for test in roadmap.parse.linked_tests:
            tid = f"test:{test}"
            nodes[tid] = {"id": tid, "type": "test", "path": test}
            edges.append({"source": tid, "target": rid, "type": "validates"})
            if not (root_path / test).exists():
                missing_tests.append(test)
        for doc in roadmap.parse.linked_docs:
            did = f"doc:{doc}"
            nodes[did] = {"id": did, "type": "doc", "path": doc}
            edges.append({"source": did, "target": rid, "type": "documents"})
            if not (root_path / doc).exists():
                unlinked_docs.append(doc)
    payload = {
        "status": "ready",
        "nodes": list(nodes.values()),
        "edges": edges,
        "summary": {
            "roadmaps": sum(1 for item in nodes.values() if item["type"] == "roadmap"),
            "modules": sum(1 for item in nodes.values() if item["type"] == "module"),
            "tests": sum(1 for item in nodes.values() if item["type"] == "test"),
            "docs": sum(1 for item in nodes.values() if item["type"] == "doc"),
            "missing_tests": sorted(dict.fromkeys(missing_tests)),
            "unlinked_docs": sorted(dict.fromkeys(unlinked_docs)),
        },
        "live_trading_enabled": False,
    }
    out_dir = Path(out) if out else root_path / "data" / "roadmaps" / "graph"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "roadmap_graph.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    (out_dir / "roadmap_graph.md").write_text(_graph_markdown(payload), encoding="utf-8")
    with (out_dir / "roadmap_dependencies.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "type"])
        writer.writeheader()
        writer.writerows(edges)
    payload["paths"] = {"json": str(out_dir / "roadmap_graph.json"), "markdown": str(out_dir / "roadmap_graph.md"), "csv": str(out_dir / "roadmap_dependencies.csv")}
    return payload


def _graph_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    return "\n".join(
        [
            "# Roadmap Dependency Graph",
            "",
            f"- Roadmaps: {summary['roadmaps']}",
            f"- Modules: {summary['modules']}",
            f"- Tests: {summary['tests']}",
            f"- Docs: {summary['docs']}",
            f"- Missing tests: {len(summary['missing_tests'])}",
            f"- Unlinked docs: {len(summary['unlinked_docs'])}",
            "- Live trading enabled: false",
            "",
        ]
    )


def roadmap_dep_graph(names: list[str]) -> dict[str, Any]:
    nodes = [{"id": name, "type": "roadmap"} for name in names]
    edges = [{"source": names[index], "target": names[index + 1], "type": "follows_on"} for index in range(max(0, len(names) - 1))]
    return {"status": "ready", "nodes": nodes, "edges": edges, "live_trading_enabled": False}
