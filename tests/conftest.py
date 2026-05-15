from __future__ import annotations

import re
import tempfile
import uuid
from pathlib import Path
from typing import Any

import pytest


_TEMP_ROOT = Path.cwd() / "data" / "pytest-tmp"
_ORIGINAL_TEMPDIR = tempfile.TemporaryDirectory
_ORIGINAL_MKDTEMP = tempfile.mkdtemp


def _safe_test_name(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")[:120] or "test"


def _safe_temp_dir(prefix: str = "tmp", suffix: str = "", dir: str | None = None) -> Path:
    root = Path(dir) if dir else _TEMP_ROOT
    try:
        root.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        root = _TEMP_ROOT
        root.mkdir(parents=True, exist_ok=True)
    path = root / f"{prefix}{uuid.uuid4().hex}{suffix}"
    path.mkdir(parents=True, exist_ok=False)
    return path


class SafeTemporaryDirectory:
    def __init__(
        self,
        suffix: str | None = None,
        prefix: str | None = None,
        dir: str | None = None,
        ignore_cleanup_errors: bool = False,
        delete: bool = True,
    ) -> None:
        self.name = str(_safe_temp_dir(prefix or "tmp", suffix or "", dir))
        self.ignore_cleanup_errors = ignore_cleanup_errors
        self.delete = delete

    def __enter__(self) -> str:
        return self.name

    def __exit__(self, *_exc: Any) -> None:
        self.cleanup()

    def cleanup(self) -> None:
        return None


def safe_mkdtemp(suffix: str | None = None, prefix: str | None = None, dir: str | None = None) -> str:
    return str(_safe_temp_dir(prefix or "tmp", suffix or "", dir))


def pytest_configure() -> None:
    tempfile.TemporaryDirectory = SafeTemporaryDirectory  # type: ignore[assignment]
    tempfile.mkdtemp = safe_mkdtemp


def pytest_unconfigure() -> None:
    tempfile.TemporaryDirectory = _ORIGINAL_TEMPDIR  # type: ignore[assignment]
    tempfile.mkdtemp = _ORIGINAL_MKDTEMP


@pytest.fixture
def tmp_path(request: pytest.FixtureRequest) -> Path:
    root = _TEMP_ROOT
    path = root / f"{_safe_test_name(request.node.nodeid)}-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    return path
