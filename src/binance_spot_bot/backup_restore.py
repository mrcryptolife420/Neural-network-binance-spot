from __future__ import annotations

import hashlib
import json
import time
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .redaction import redact_payload, redact_text


@dataclass(frozen=True)
class BackupManifest:
    created_at_ms: int
    files: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def create_backup(paths: Iterable[Path], output_zip: Path) -> BackupManifest:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    files: dict[str, str] = {}
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for root in paths:
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_file() and _allowed(path):
                    data = _redacted_bytes(path)
                    arcname = str(path.relative_to(root.parent)).replace("\\", "/")
                    archive.writestr(arcname, data)
                    files[arcname] = hashlib.sha256(data).hexdigest()
        manifest = BackupManifest(int(time.time() * 1000), files)
        archive.writestr("manifest.json", json.dumps(manifest.to_dict(), indent=2))
    return manifest


def restore_backup(backup_zip: Path, target_dir: Path, confirm: bool = False) -> list[Path]:
    if not confirm:
        raise ValueError("restore requires explicit confirmation")
    target_dir.mkdir(parents=True, exist_ok=True)
    restored: list[Path] = []
    with zipfile.ZipFile(backup_zip, "r") as archive:
        for member in archive.namelist():
            if member == "manifest.json":
                continue
            target = (target_dir / member).resolve()
            if target.exists():
                raise FileExistsError(f"refusing to overwrite {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
            restored.append(target)
    return restored


def _allowed(path: Path) -> bool:
    return path.suffix.lower() in {".json", ".jsonl", ".md", ".csv", ".txt", ".toml", ".example"}


def _redacted_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".json":
        try:
            return json.dumps(redact_payload(json.loads(text)), indent=2).encode("utf-8")
        except json.JSONDecodeError:
            pass
    return redact_text(text).encode("utf-8")
