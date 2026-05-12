from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .roadmap_index import RoadmapIndex, build_roadmap_index_object


def _legacy_name_guard(names: list[str]) -> dict[str, Any]:
    counts = Counter(names)
    duplicates = sorted(name for name, count in counts.items() if count > 1)
    return {"status": "blocked" if duplicates else "ok", "duplicates": duplicates, "live_trading_enabled": False}


def run_roadmap_duplicate_guard(root: Path | str = ".", number: int | None = None, index: RoadmapIndex | None = None) -> dict[str, Any]:
    idx = index or build_roadmap_index_object(root)
    by_number: dict[int, list[dict[str, Any]]] = {}
    title_counts: Counter[str] = Counter()
    blockers: list[str] = []
    warnings: list[str] = []
    for roadmap in idx.roadmaps:
        if roadmap.number is not None:
            by_number.setdefault(roadmap.number, []).append(roadmap.to_dict())
        title_counts[roadmap.title.lower()] += 1
        if roadmap.parse.filename_number and roadmap.parse.title_number and roadmap.parse.filename_number != roadmap.parse.title_number:
            blockers.append(f"filename_title_mismatch:{roadmap.path}")
        if roadmap.status == "unknown":
            warnings.append(f"missing_status:{roadmap.path}")
        if roadmap.parse.definition_of_done_count == 0:
            warnings.append(f"missing_definition_of_done:{roadmap.path}")
        if not roadmap.parse.has_acceptance_criteria:
            warnings.append(f"missing_acceptance_criteria:{roadmap.path}")
    duplicate_numbers = {key: value for key, value in by_number.items() if len(value) > 1}
    duplicate_titles = sorted(title for title, count in title_counts.items() if count > 1)
    if duplicate_numbers:
        blockers.extend(f"duplicate_number:{number}" for number in sorted(duplicate_numbers))
    if number is not None and number in by_number:
        blockers.append(f"number_already_exists:{number:03d}")
    completed_keys = {(item.number, item.title.lower()) for item in idx.roadmaps if item.location == "voltooid_docs"}
    for item in idx.roadmaps:
        if item.location == "roadmap_docs" and (item.number, item.title.lower()) in completed_keys:
            blockers.append(f"already_completed:{item.path}")
    status = "blocked" if blockers else ("warning" if warnings or duplicate_titles else "ok")
    return {
        "status": status,
        "highest_number": idx.number_status.highest_number,
        "next_number": idx.number_status.next_number,
        "duplicate_numbers": sorted(duplicate_numbers),
        "duplicate_titles": duplicate_titles,
        "blockers": sorted(dict.fromkeys(blockers)),
        "warnings": sorted(dict.fromkeys(warnings)),
        "live_trading_enabled": False,
    }


def roadmap_duplicate_guard(names: list[str] | None = None, *, root: Path | str = ".", number: int | None = None) -> dict[str, Any]:
    if names is not None:
        return _legacy_name_guard(names)
    return run_roadmap_duplicate_guard(root=root, number=number)
