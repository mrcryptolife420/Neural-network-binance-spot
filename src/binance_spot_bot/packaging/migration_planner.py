from __future__ import annotations


def preview_package_migration(schema_known: bool = True, dry_run: bool = True) -> dict[str, object]:
    blockers = []
    if not schema_known:
        blockers.append("unknown schema")
    if not dry_run:
        blockers.append("dry-run required before apply")
    return {"status": "blocked" if blockers else "ok", "mode": "preview", "targets": ["profiles", "workspaces", "sessions", "evidence", "live_ops_incidents"], "blockers": blockers, "live_trading_enabled": False}

