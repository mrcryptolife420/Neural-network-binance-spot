from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .redaction import redact_payload

ROADMAP_RE = re.compile(r"^(?P<number>\d{3})-.*\.md$")


def _roadmap_files(root: Path) -> list[tuple[str, str, Path]]:
    rows: list[tuple[str, str, Path]] = []
    for status, directory in (("open", root / "Roadmap docs"), ("completed", root / "Voltooid docs")):
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            match = ROADMAP_RE.match(path.name)
            if match:
                rows.append((match.group("number"), status, path))
    return rows


def build_roadmap_milestone_traceability(root: Path | str = ".", start: int = 1, end: int = 100) -> dict[str, Any]:
    root = Path(root)
    rows = _roadmap_files(root)
    by_number: dict[str, list[dict[str, Any]]] = {}
    tests = list((root / "tests").glob("test*.py")) if (root / "tests").exists() else []
    docs = list((root / "docs").glob("*.md")) if (root / "docs").exists() else []
    for number, status, path in rows:
        if start <= int(number) <= end:
            content = path.read_text(encoding="utf-8", errors="ignore")
            by_number.setdefault(number, []).append(
                {
                    "number": number,
                    "status": status,
                    "path": str(path.relative_to(root)),
                    "has_definition_of_done": "definition of done" in content.lower(),
                    "tests": [str(test.relative_to(root)) for test in tests if number in test.name],
                    "docs": [str(doc.relative_to(root)) for doc in docs if number in doc.name],
                }
            )
    expected = [f"{number:03d}" for number in range(start, end + 1)]
    missing = [number for number in expected if number not in by_number]
    duplicates = [number for number, matches in by_number.items() if len(matches) > 1]
    completed_without_evidence = [
        number
        for number, matches in by_number.items()
        if any(match["status"] == "completed" for match in matches) and not any(match["tests"] or match["docs"] for match in matches)
    ]
    payload = {
        "status": "review" if missing or duplicates or completed_without_evidence else "ok",
        "range": f"{start:03d}-{end:03d}",
        "roadmaps": by_number,
        "missing": missing,
        "duplicates": duplicates,
        "completed_without_evidence": completed_without_evidence,
        "live_trading_enabled": False,
    }
    return redact_payload(payload)


def roadmap_milestone_traceability(root: Path | str = ".") -> dict[str, Any]:
    return build_roadmap_milestone_traceability(root)


def write_roadmap_milestone_traceability(root: Path | str = ".", out_dir: Path | str | None = None) -> dict[str, str]:
    root = Path(root)
    out = Path(out_dir) if out_dir else root / "data" / "milestone" / "roadmap-traceability"
    out.mkdir(parents=True, exist_ok=True)
    payload = build_roadmap_milestone_traceability(root)
    json_path = out / "roadmap_traceability_001_100.json"
    md_path = out / "roadmap_traceability_001_100.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Roadmap Traceability 001-100",
                "",
                f"Status: {payload['status']}",
                f"Missing: {len(payload['missing'])}",
                f"Duplicates: {len(payload['duplicates'])}",
                "Live trading: disabled",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
