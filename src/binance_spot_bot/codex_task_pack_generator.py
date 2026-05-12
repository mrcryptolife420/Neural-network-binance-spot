from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .codex_task_packs import CodexFileBoundary, CodexTask, CodexTaskPack, FORBIDDEN_FILES, SAFETY_CONSTRAINTS
from .roadmap_index import build_roadmap_index_object


DEFAULT_PHASES = [
    ("foundation", ["src/binance_spot_bot/roadmap_index.py", "src/binance_spot_bot/roadmap_duplicate_guard.py"]),
    ("graph", ["src/binance_spot_bot/roadmap_dependency_graph.py"]),
    ("task-packs", ["src/binance_spot_bot/codex_task_packs.py", "src/binance_spot_bot/codex_task_pack_generator.py"]),
    ("validation", ["src/binance_spot_bot/roadmap_validation.py", "src/binance_spot_bot/roadmap_completion_gate.py"]),
    ("evidence-dashboard-cli", ["src/binance_spot_bot/cli.py", "src/binance_spot_bot/ui/streamlit_app.py", "docs/*"]),
]


def generate_codex_task_packs(root: Path | str = ".", roadmap: int | str | None = None, out: Path | str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    idx = build_roadmap_index_object(root_path)
    number = int(str(roadmap).lstrip("0") or "0") if roadmap is not None else idx.number_status.highest_number
    selected = next((item for item in idx.roadmaps if item.number == number), None)
    title = selected.title if selected else f"Roadmap {number:03d}"
    tasks: list[CodexTask] = []
    for index, (phase, allowed) in enumerate(DEFAULT_PHASES, start=1):
        tasks.append(
            CodexTask(
                task_id=f"pr-{index:02d}",
                title=f"{title} - {phase}",
                goal=f"Implement and validate the {phase} slice without rebuilding existing infrastructure.",
                phase=phase,
                file_boundary=CodexFileBoundary(allowed, FORBIDDEN_FILES),
                required_tests=["python -m pytest tests/test_roadmap_090_roadmap_execution_acceptance.py -q", "python -m binance_spot_bot.cli check-all --skip-tests --json"],
                required_docs=["docs/roadmap-execution-cli.md", "docs/roadmap-execution-dashboard.md"],
                required_evidence=[f"data/roadmaps/evidence/{number:03d}/roadmap_evidence_manifest.json"],
                safety_constraints=SAFETY_CONSTRAINTS,
                validation_commands=["python -m pytest -q", "python -m binance_spot_bot.cli dashboard-smoke --seconds 1"],
                acceptance_criteria=["scope boundaries respected", "reports are secret-free", "live_trading_enabled=false"],
                rollback_notes="Use git diff to revert only files listed in the task boundary.",
            )
        )
    pack = CodexTaskPack(f"roadmap-{number:03d}", number, title, tasks)
    payload = {"status": "ready", "task_pack": pack.to_dict(), "live_trading_enabled": False}
    out_dir = Path(out) if out else root_path / "data" / "roadmaps" / "task-packs" / f"{number:03d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    for task in tasks:
        task_payload = {**pack.to_dict(), "tasks": [task.to_dict()]}
        (out_dir / f"{task.task_id}-task-pack.json").write_text(json.dumps(task_payload, indent=2, default=str), encoding="utf-8")
        (out_dir / f"{task.task_id}-task-pack.md").write_text(_task_markdown(pack, task), encoding="utf-8")
    payload["path"] = str(out_dir)
    return payload


def _task_markdown(pack: CodexTaskPack, task: CodexTask) -> str:
    return "\n".join(
        [
            f"# {task.title}",
            "",
            f"Roadmap: {pack.roadmap_number:03d} - {pack.roadmap_title}",
            f"Goal: {task.goal}",
            "",
            "Allowed files:",
            *(f"- {item}" for item in task.file_boundary.allowed_files),
            "",
            "Forbidden files:",
            *(f"- {item}" for item in task.file_boundary.forbidden_files),
            "",
            "Validation:",
            *(f"- `{item}`" for item in task.validation_commands),
            "",
            "Safety:",
            *(f"- {item}" for item in task.safety_constraints),
            "- Live trading enabled: false",
            "",
        ]
    )
