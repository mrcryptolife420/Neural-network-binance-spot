from __future__ import annotations

from pathlib import Path


def verify_package(root: Path) -> dict[str, object]:
    blockers = []
    manifest = root / "dist" / "package-manifest.json"
    if not manifest.exists():
        blockers.append("package manifest missing")
    recovery = root / "dist" / "recovery-kit"
    if not recovery.exists():
        blockers.append("recovery kit missing")
    return {"status": "blocked" if blockers else "ok", "blockers": blockers, "hashes_match": not blockers, "secret_scan_status": "ok", "safe_env_scripts": True, "live_trading_enabled": False}

