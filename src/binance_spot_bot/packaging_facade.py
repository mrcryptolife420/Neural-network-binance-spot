from __future__ import annotations

from pathlib import Path

from .local_paper_os_facade import safe_record, write_json_report


def production_packaging_plan() -> dict:
    return safe_record("production_packaging", {"installer": "local-windows", "desktop_shortcut": True, "safe_update": True, "rollback": True, "offline_recovery": True})


def safe_update_plan(version: str) -> dict:
    return safe_record("safe_update_plan", {"version": version, "requires_backup": True, "rollback_test_required": True})


def offline_recovery_kit(files: list[Path], out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    return safe_record("offline_recovery_kit", {"files": [str(path) for path in files], "out": str(out)})


def write_packaging_report(root: Path, payload: dict) -> dict[str, str]:
    return write_json_report(root, "packaging", "production-packaging", payload)
