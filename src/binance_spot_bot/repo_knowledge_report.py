from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .artifact_flow_graph import build_artifact_flow_graph
from .cli_surface_map import build_cli_surface_map
from .code_graph import build_code_graph
from .dashboard_surface_map import build_dashboard_surface_map
from .repo_inventory import build_repo_inventory


def build_repo_knowledge_report(root: Path | str = ".") -> dict[str, Any]:
    root_path = Path(root)
    inventory = build_repo_inventory(root_path)
    graph = build_code_graph(root_path)
    cli = build_cli_surface_map(root_path)
    dashboard = build_dashboard_surface_map(root_path)
    artifacts = build_artifact_flow_graph(root_path)
    return {
        "status": "ready",
        "summary": {
            "files": len(inventory["payload"]["files"]),
            "modules": len(graph["payload"]["nodes"]),
            "cli_commands": cli["payload"]["count"],
            "dashboard_panels": len(dashboard["payload"]["panels"]),
            "artifact_roots": len(artifacts["nodes"]),
        },
        "top_central_modules": graph["payload"]["high_fan_in"][:10],
        "large_modules": graph["payload"]["large_modules"][:10],
        "live_trading_enabled": False,
    }


def write_repo_knowledge_report(root: Path, payload: dict | None = None) -> dict[str, str]:
    report = payload or build_repo_knowledge_report(root)
    out = root / "data" / "repository-knowledge" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "repository_knowledge_report.json"
    md_path = out / "repository_knowledge_report.md"
    json_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Repository Knowledge Report",
                "",
                f"- Files: {report['summary']['files']}",
                f"- Modules: {report['summary']['modules']}",
                f"- CLI commands: {report['summary']['cli_commands']}",
                f"- Dashboard panels: {report['summary']['dashboard_panels']}",
                "- Live trading enabled: false",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
