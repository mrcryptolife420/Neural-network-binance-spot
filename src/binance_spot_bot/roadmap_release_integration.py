from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .roadmap_index import build_roadmap_index_object


def generate_roadmap_release_input(root: Path | str = ".", out: Path | str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    idx = build_roadmap_index_object(root_path)
    completed = [item for item in idx.roadmaps if item.location == "voltooid_docs"]
    open_items = [item for item in idx.roadmaps if item.location == "roadmap_docs"]
    payload = {
        "status": "ready",
        "completed": [{"number": item.number, "title": item.title, "path": item.path} for item in completed[-20:]],
        "open": [{"number": item.number, "title": item.title, "path": item.path} for item in open_items[:20]],
        "dashboard_changes": [item.number for item in idx.roadmaps if "dashboard" in item.title.lower()],
        "migration_changes": [item.number for item in idx.roadmaps if "migration" in item.title.lower()],
        "validation_commands": ["python -m pytest -q", "python -m binance_spot_bot.cli check-all --skip-tests --json"],
        "live_trading_enabled": False,
    }
    out_dir = Path(out) if out else root_path / "data" / "roadmaps" / "release-input"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "roadmap-release-input.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    (out_dir / "roadmap-release-input.md").write_text(_markdown(payload), encoding="utf-8")
    payload["paths"] = {"json": str(out_dir / "roadmap-release-input.json"), "markdown": str(out_dir / "roadmap-release-input.md")}
    return payload


def _markdown(payload: dict[str, Any]) -> str:
    lines = ["# Roadmap Release Input", "", f"- Completed sample: {len(payload['completed'])}", f"- Open sample: {len(payload['open'])}", "- Live trading enabled: false", ""]
    lines.extend(f"- Completed {item['number']}: {item['title']}" for item in payload["completed"])
    return "\n".join(lines) + "\n"


def roadmap_release_integration(roadmaps: list[str]) -> dict[str, Any]:
    return {"status": "ready", "roadmaps": roadmaps, "release_notes_input": roadmaps, "live_trading_enabled": False}
