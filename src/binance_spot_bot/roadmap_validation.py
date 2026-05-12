from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .roadmap_index import parse_roadmap_file


def validate_roadmap_file(path: Path | str, root: Path | str | None = None) -> dict[str, Any]:
    file_path = Path(path)
    roadmap = parse_roadmap_file(file_path, "validation", Path(root).resolve() if root else None)
    text = file_path.read_text(encoding="utf-8-sig", errors="ignore")
    return _validate(text, roadmap.path, roadmap.parse.filename_number, roadmap.parse.title_number)


def validate_roadmap_text(text: str) -> dict[str, Any]:
    return _validate(text, "<text>", None, None)


def _validate(text: str, path: str, filename_number: int | None, title_number: int | None) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    required = {
        "status": r"^Status:",
        "phases": r"Fase|Phase|PR \d+",
        "definition_of_done": r"Definition of Done",
        "tests": r"Tests|Test Plan|Validatie",
        "docs": r"Docs|Nieuwe docs|Documentatie",
        "safety": r"Geen live trading|No live|live trading.*disabled",
        "codex_task": r"Beste eerste Codex|Codex",
        "acceptance": r"Acceptatiecriteria|Acceptance criteria",
    }
    for name, pattern in required.items():
        if not re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            blockers.append(f"missing_{name}")
    if filename_number and title_number and filename_number != title_number:
        blockers.append("filename_title_number_mismatch")
    if "[ ]" not in text and "[x]" not in text.lower():
        warnings.append("no_parseable_checkboxes")
    linked_tests = re.findall(r"tests/[^\s`)]+", text)
    linked_modules = re.findall(r"src/[^\s`)]+", text)
    status = "blocked" if blockers else ("warning" if warnings else "ok")
    payload = {
        "status": status,
        "path": path,
        "blockers": blockers,
        "warnings": warnings,
        "linked_tests": sorted(dict.fromkeys(linked_tests)),
        "linked_modules": sorted(dict.fromkeys(linked_modules)),
        "live_trading_enabled": False,
    }
    return payload


def write_roadmap_validation_report(payload: dict[str, Any], out: Path | str) -> dict[str, Any]:
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "roadmap_validation_report.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    lines = ["# Roadmap Validation Report", "", f"- Status: {payload['status']}"]
    lines.extend(f"- Blocker: {item}" for item in payload.get("blockers", []))
    lines.extend(f"- Warning: {item}" for item in payload.get("warnings", []))
    lines.append("- Live trading enabled: false")
    (out_dir / "roadmap_validation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {**payload, "paths": {"json": str(out_dir / "roadmap_validation_report.json"), "markdown": str(out_dir / "roadmap_validation_report.md")}}
