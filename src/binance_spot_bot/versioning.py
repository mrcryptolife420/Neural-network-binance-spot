from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import time
import tomllib
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class ProjectVersion:
    version: str
    source: str
    package_installed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class VersionComponent:
    name: str
    version: str
    status: str = "ok"

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class InstallFingerprint:
    version: str
    python_version: str
    platform_name: str
    git_available: bool
    git_commit: str = ""
    git_dirty: bool = False
    data_dir_hash: str = ""
    components: list[VersionComponent] = field(default_factory=list)
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = {**asdict(self), "components": [item.to_dict() for item in self.components], "live_trading_enabled": False}
        payload["fingerprint_hash"] = _hash(payload)
        return redact_payload(payload)


@dataclass(frozen=True)
class VersionCheckResult:
    status: str
    current: str
    target: str = ""
    reasons: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def detect_project_version(root: Path | str = ".") -> ProjectVersion:
    pyproject = Path(root) / "pyproject.toml"
    if pyproject.exists():
        try:
            payload = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            return ProjectVersion(str(payload.get("project", {}).get("version", "0.0.0")), "pyproject", False)
        except Exception:
            pass
    try:
        return ProjectVersion(importlib.metadata.version("neural-network-binance-spot"), "package_metadata", True)
    except importlib.metadata.PackageNotFoundError:
        return ProjectVersion("0.0.0", "fallback", False)


def build_install_fingerprint(root: Path | str = ".", data_dir: Path | str = "data") -> dict[str, Any]:
    version = detect_project_version(root)
    commit, dirty, git_available = _git_state(Path(root))
    fingerprint = InstallFingerprint(
        version=version.version,
        python_version=sys.version.split()[0],
        platform_name=platform.platform(),
        git_available=git_available,
        git_commit=commit[:16],
        git_dirty=dirty,
        data_dir_hash=_hash(str(Path(data_dir).resolve())),
        components=[
            VersionComponent("config_schema", "1"),
            VersionComponent("data_schema", "1"),
            VersionComponent("metrics_schema", "1"),
            VersionComponent("permission_schema", "1"),
            VersionComponent("backup_schema", "1"),
        ],
    )
    payload = {"status": "ok", "payload": fingerprint.to_dict(), "version_source": version.source, "live_trading_enabled": False}
    out = Path(data_dir) / "releases"
    out.mkdir(parents=True, exist_ok=True)
    (out / "current-install-fingerprint.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return payload


def version_payload(version: str | None = None) -> dict[str, Any]:
    detected = detect_project_version()
    value = version or detected.version
    return {"status": "ok", "payload": {"version": value, "source": "argument" if version else detected.source, "schema_version": "1", "live_trading_enabled": False}, "live_trading_enabled": False}


def _git_state(root: Path) -> tuple[str, bool, bool]:
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True, text=True, check=False, timeout=5).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=str(root), capture_output=True, text=True, check=False, timeout=5).stdout.strip())
        return commit, dirty, bool(commit)
    except Exception:
        return "", False, False


def _hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(redact_payload(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:24]
