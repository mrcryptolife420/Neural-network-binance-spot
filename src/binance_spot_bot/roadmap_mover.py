from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from .roadmap_completion_gate import evaluate_roadmap_completion_gate

CONFIRM_PHRASE = "MOVE_ROADMAP_TO_VOLTOOID"


def _short_file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:24]


def roadmap_move_plan(src: Path, dst: Path) -> dict[str, Any]:
    return {
        "status": "ready" if src.exists() and not dst.exists() else "blocked",
        "source": str(src),
        "target": str(dst),
        "source_exists": src.exists(),
        "target_exists": dst.exists(),
        "live_trading_enabled": False,
    }


def move_completed_roadmap(
    root: Path | str,
    roadmap: int | str,
    *,
    confirm: str = "",
    evidence: dict[str, Any] | None = None,
    dry_run: bool = True,
) -> dict[str, Any]:
    root_path = Path(root)
    number = f"{int(str(roadmap).lstrip('0') or '0'):03d}"
    matches = sorted((root_path / "Roadmap docs").glob(f"{number}-roadmap-*.md"))
    if not matches:
        return {"status": "blocked", "reason": "source_missing", "roadmap": number, "live_trading_enabled": False}
    src = matches[0]
    dst = root_path / "Voltooid docs" / src.name
    plan = roadmap_move_plan(src, dst)
    gate = evaluate_roadmap_completion_gate(number, evidence=evidence or {})
    blockers = []
    if plan["status"] != "ready":
        blockers.append("move_plan_blocked")
    if gate["status"] != "ready_to_complete":
        blockers.extend(gate["blockers"])
    if not dry_run and confirm != CONFIRM_PHRASE:
        blockers.append("confirm_phrase_required")
    status = "blocked" if blockers else ("dry_run" if dry_run else "moved")
    manifest = {
        "status": status,
        "roadmap": number,
        "source": str(src),
        "target": str(dst),
        "source_sha256": _short_file_hash(src) if src.exists() else "",
        "completion_gate": gate,
        "blockers": blockers,
        "live_trading_enabled": False,
    }
    if blockers or dry_run:
        return manifest
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    manifest["target_sha256"] = _short_file_hash(dst)
    out_dir = root_path / "data" / "roadmaps" / "moves"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / f"{number}-move-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    manifest["manifest"] = str(manifest_path)
    return manifest
