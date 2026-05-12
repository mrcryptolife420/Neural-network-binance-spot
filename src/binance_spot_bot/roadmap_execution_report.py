from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .roadmap_completion_gate import evaluate_roadmap_completion_gate
from .roadmap_duplicate_guard import run_roadmap_duplicate_guard
from .roadmap_index import build_roadmap_index_object


def build_roadmap_execution_report(root: Path | str = ".") -> dict[str, Any]:
    root_path = Path(root)
    idx = build_roadmap_index_object(root_path)
    duplicate_guard = run_roadmap_duplicate_guard(root_path, index=idx)
    active = [item for item in idx.roadmaps if item.location == "roadmap_docs"]
    report = {
        "status": "ready",
        "active_roadmaps": len(active),
        "blocked_roadmaps": len(duplicate_guard["blockers"]),
        "task_packs_generated": len(list((root_path / "data" / "roadmaps" / "task-packs").glob("*"))) if (root_path / "data" / "roadmaps" / "task-packs").exists() else 0,
        "duplicate_guard": duplicate_guard,
        "next_codex_task": active[0].title if active else "",
        "completion_gate_sample": evaluate_roadmap_completion_gate("090", evidence={"tests_passed": True, "check_all_passed": True, "no_live_proof": True}),
        "live_trading_enabled": False,
    }
    return report


def write_roadmap_execution_report(root: Path, payload: dict[str, Any] | None = None) -> dict[str, str]:
    report = payload or build_roadmap_execution_report(root)
    out = root / "data" / "roadmaps" / "reports" / "daily"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "roadmap-execution-report.json"
    md_path = out / "roadmap-execution-report.md"
    json_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Roadmap Execution Report",
                "",
                f"- Active roadmaps: {report['active_roadmaps']}",
                f"- Blocked roadmaps: {report['blocked_roadmaps']}",
                f"- Next Codex task: {report['next_codex_task']}",
                "- Live trading enabled: false",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}


def write_roadmap_exec_report(root: Path, payload: dict) -> dict[str, str]:
    return write_roadmap_execution_report(root, payload)
