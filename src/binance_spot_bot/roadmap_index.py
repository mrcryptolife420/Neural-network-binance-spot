from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROADMAP_NAME_RE = re.compile(r"(?P<number>\d{3})-roadmap-(?P<slug>.+)\.md$", re.IGNORECASE)
ROADMAP_TITLE_RE = re.compile(r"^\s*#\s*Roadmap\s+(?P<number>\d{3})\s*-\s*(?P<title>.+)$", re.IGNORECASE | re.MULTILINE)
STATUS_RE = re.compile(r"^\s*Status:\s*(?P<status>.+)$", re.IGNORECASE | re.MULTILINE)
PATH_RE = re.compile(r"(?P<path>(?:src|tests|docs|Roadmap docs|Voltooid docs)/[^\s`)]+)", re.IGNORECASE)


@dataclass(frozen=True)
class RoadmapLocation:
    name: str
    directory: str
    completed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RoadmapParseResult:
    filename_number: int | None
    title_number: int | None
    title: str
    status: str
    checkbox_count: int
    checked_count: int
    unchecked_count: int
    follows_on: list[int]
    linked_tests: list[str]
    linked_docs: list[str]
    linked_modules: list[str]
    definition_of_done_count: int
    has_acceptance_criteria: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RoadmapFile:
    number: int | None
    title: str
    status: str
    path: str
    location: str
    modified_at: float
    sha256: str
    parse: RoadmapParseResult

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["live_trading_enabled"] = False
        return payload


@dataclass(frozen=True)
class RoadmapNumberStatus:
    highest_number: int
    next_number: int
    missing_numbers: list[int]
    duplicate_numbers: list[int]

    def to_dict(self) -> dict[str, Any]:
        return {**asdict(self), "live_trading_enabled": False}


@dataclass(frozen=True)
class RoadmapIndex:
    root: str
    locations: list[RoadmapLocation]
    roadmaps: list[RoadmapFile]
    number_status: RoadmapNumberStatus

    def to_dict(self) -> dict[str, Any]:
        open_count = sum(1 for item in self.roadmaps if item.location == "roadmap_docs")
        done_count = sum(1 for item in self.roadmaps if item.location == "voltooid_docs")
        return {
            "status": "ready",
            "root": self.root,
            "payload": {
                "open_count": open_count,
                "done_count": done_count,
                "total_count": len(self.roadmaps),
                "highest_number": self.number_status.highest_number,
                "next_number": self.number_status.next_number,
                "duplicates": self.number_status.duplicate_numbers,
                "missing_numbers": self.number_status.missing_numbers,
                "roadmaps": [item.to_dict() for item in self.roadmaps],
                "locations": [item.to_dict() for item in self.locations],
            },
            "live_trading_enabled": False,
        }


def _location_specs(root: Path) -> list[RoadmapLocation]:
    return [
        RoadmapLocation("voltooid_docs", str(root / "Voltooid docs"), True),
        RoadmapLocation("roadmap_docs", str(root / "Roadmap docs"), False),
        RoadmapLocation("docs", str(root / "docs"), False),
        RoadmapLocation("runbooks", str(root / "docs" / "runbooks"), False),
    ]


def _short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:24]


def _dedupe(values: list[str]) -> list[str]:
    return sorted(dict.fromkeys(values))


def parse_roadmap_file(path: Path, location: str, root: Path | None = None) -> RoadmapFile:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    name_match = ROADMAP_NAME_RE.search(path.name)
    title_match = ROADMAP_TITLE_RE.search(text)
    status_match = STATUS_RE.search(text)
    filename_number = int(name_match.group("number")) if name_match else None
    title_number = int(title_match.group("number")) if title_match else None
    title = title_match.group("title").strip() if title_match else path.stem
    status = status_match.group("status").strip() if status_match else "unknown"
    checked = len(re.findall(r"\[[xX]\]", text))
    unchecked = len(re.findall(r"\[ \]", text))
    paths = _dedupe([match.group("path").rstrip(".,") for match in PATH_RE.finditer(text)])
    follows_on = sorted({int(value) for value in re.findall(r"(?:Roadmap docs|Voltooid docs)/(\d{3})-roadmap", text)})
    parse = RoadmapParseResult(
        filename_number=filename_number,
        title_number=title_number,
        title=title,
        status=status,
        checkbox_count=checked + unchecked,
        checked_count=checked,
        unchecked_count=unchecked,
        follows_on=follows_on,
        linked_tests=[item for item in paths if item.startswith("tests/")],
        linked_docs=[item for item in paths if item.startswith("docs/")],
        linked_modules=[item for item in paths if item.startswith("src/")],
        definition_of_done_count=len(re.findall(r"Definition of Done", text, flags=re.IGNORECASE)),
        has_acceptance_criteria=bool(re.search(r"Acceptatiecriteria|Acceptance criteria", text, re.IGNORECASE)),
    )
    display_path = str(path.relative_to(root)) if root and path.is_relative_to(root) else str(path)
    return RoadmapFile(
        number=filename_number or title_number,
        title=title,
        status=status,
        path=display_path.replace("\\", "/"),
        location=location,
        modified_at=path.stat().st_mtime,
        sha256=_short_hash(text),
        parse=parse,
    )


def build_roadmap_index_object(root: Path | str = ".") -> RoadmapIndex:
    root_path = Path(root).resolve()
    specs = _location_specs(root_path)
    roadmaps: list[RoadmapFile] = []
    seen_paths: set[Path] = set()
    for spec in specs:
        directory = Path(spec.directory)
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.md")):
            if path in seen_paths:
                continue
            if ROADMAP_NAME_RE.search(path.name) or ROADMAP_TITLE_RE.search(path.read_text(encoding="utf-8-sig", errors="ignore")[:400]):
                seen_paths.add(path)
                roadmaps.append(parse_roadmap_file(path, spec.name, root_path))
    numbers = sorted(item.number for item in roadmaps if item.number is not None)
    duplicates = sorted({number for number in numbers if numbers.count(number) > 1})
    highest = max(numbers, default=0)
    missing = [number for number in range(min(numbers, default=1), highest + 1) if number not in numbers]
    status = RoadmapNumberStatus(highest_number=highest, next_number=highest + 1, missing_numbers=missing, duplicate_numbers=duplicates)
    return RoadmapIndex(str(root_path), specs, sorted(roadmaps, key=lambda item: (item.number or 9999, item.path)), status)


def build_roadmap_index(root: Path | str = ".") -> dict[str, Any]:
    return build_roadmap_index_object(root).to_dict()


def find_next_roadmap_number(index: RoadmapIndex | dict[str, Any]) -> int:
    if isinstance(index, RoadmapIndex):
        return index.number_status.next_number
    return int(index.get("payload", {}).get("next_number", 1))
