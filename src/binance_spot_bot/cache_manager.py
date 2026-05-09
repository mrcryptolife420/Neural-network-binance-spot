from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CacheEntry:
    path: str
    size_bytes: int
    modified_at_ms: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def cache_manifest(root: Path) -> dict[str, Any]:
    entries = []
    for path in root.rglob("*") if root.exists() else []:
        if path.is_file():
            stat = path.stat()
            entries.append(CacheEntry(str(path), stat.st_size, int(stat.st_mtime * 1000)).to_dict())
    return {"created_at_ms": int(time.time() * 1000), "entries": entries}


def write_cache_manifest(root: Path, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache_manifest(root), indent=2), encoding="utf-8")
    return path


def archive_old_cache(root: Path, archive_dir: Path, older_than_ms: int, active_session_ids: set[str] | None = None) -> list[Path]:
    active_session_ids = active_session_ids or set()
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived: list[Path] = []
    now_ms = int(time.time() * 1000)
    if not root.exists():
        return archived
    for path in root.rglob("*"):
        if not path.is_file() or any(session_id in str(path) for session_id in active_session_ids):
            continue
        if now_ms - int(path.stat().st_mtime * 1000) > older_than_ms:
            target = archive_dir / path.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            path.replace(target)
            archived.append(target)
    return archived
