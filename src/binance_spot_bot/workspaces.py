from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class WorkspaceProfile:
    name: str
    data_dir: str
    exchange_profile: str
    symbols: list[str]
    risk_preset: str = "balanced"
    theme: str = "system"
    language: str = "nl"
    layout: dict[str, Any] = field(default_factory=dict)
    notes: str = ""
    schema_version: int = 1
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    last_opened_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    archived: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class WorkspaceStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, profile: WorkspaceProfile) -> Path:
        path = self.root / f"{_safe_name(profile.name)}.json"
        path.write_text(json.dumps(profile.to_dict(), indent=2), encoding="utf-8")
        return path

    def create(
        self,
        name: str,
        *,
        data_dir: str,
        exchange_profile: str = "local-demo",
        symbols: list[str] | None = None,
        risk_preset: str = "balanced",
    ) -> WorkspaceProfile:
        profile = WorkspaceProfile(name, data_dir, exchange_profile, symbols or ["BTCUSDT"], risk_preset=risk_preset)
        self.save(profile)
        return profile

    def load(self, name: str) -> WorkspaceProfile:
        payload = json.loads((self.root / f"{_safe_name(name)}.json").read_text(encoding="utf-8"))
        return _profile_from_payload(payload)

    def touch(self, name: str) -> WorkspaceProfile:
        profile = replace(self.load(name), last_opened_at_ms=int(time.time() * 1000))
        self.save(profile)
        return profile

    def rename(self, old_name: str, new_name: str) -> WorkspaceProfile:
        profile = self.load(old_name)
        old_path = self.root / f"{_safe_name(old_name)}.json"
        new_profile = replace(profile, name=new_name, last_opened_at_ms=int(time.time() * 1000))
        self.save(new_profile)
        if old_path.exists() and old_path != self.root / f"{_safe_name(new_name)}.json":
            old_path.unlink()
        return new_profile

    def duplicate(self, source_name: str, new_name: str) -> WorkspaceProfile:
        source = self.load(source_name)
        now = int(time.time() * 1000)
        duplicate = replace(source, name=new_name, created_at_ms=now, last_opened_at_ms=now, archived=False)
        self.save(duplicate)
        return duplicate

    def archive(self, name: str, confirm: bool = False) -> WorkspaceProfile:
        if not confirm:
            raise ValueError("archive requires explicit confirmation")
        profile = replace(self.load(name), archived=True, last_opened_at_ms=int(time.time() * 1000))
        self.save(profile)
        return profile

    def export_workspace(self, name: str, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.load(name).to_dict(), indent=2), encoding="utf-8")
        return path

    def import_workspace(self, path: Path, *, overwrite: bool = False) -> WorkspaceProfile:
        profile = _profile_from_payload(json.loads(path.read_text(encoding="utf-8")))
        target = self.root / f"{_safe_name(profile.name)}.json"
        if target.exists() and not overwrite:
            raise FileExistsError(f"workspace already exists: {profile.name}")
        self.save(profile)
        return profile

    def list(self) -> list[WorkspaceProfile]:
        profiles = [_profile_from_payload(json.loads(path.read_text(encoding="utf-8"))) for path in self.root.glob("*.json")]
        profiles.sort(key=lambda item: item.name.lower())
        return profiles


def _safe_name(name: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in name.strip().lower())
    if not cleaned:
        raise ValueError("workspace name is required")
    return cleaned


def _profile_from_payload(payload: dict[str, Any]) -> WorkspaceProfile:
    fields = WorkspaceProfile.__dataclass_fields__
    clean = {key: value for key, value in payload.items() if key in fields}
    return WorkspaceProfile(**clean)
