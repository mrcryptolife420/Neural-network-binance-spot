from __future__ import annotations

from pathlib import Path
from typing import Any

from .backup_restore import create_package_backup, restore_preview
from .build_manifest import write_package_manifest
from .dependency_lock import write_dependency_lock
from .installed_startup_health import installed_startup_health
from .migration_planner import preview_package_migration
from .offline_recovery_kit import build_offline_recovery_kit
from .package_evidence import export_package_evidence
from .package_profiles import build_package_profile_report, write_package_profile_report
from .package_verify import verify_package
from .portable_bundle import build_portable_bundle
from .rollback_manager import create_rollback_point, rollback_preview
from .safe_mode import package_safe_mode_status
from .shortcuts import generate_shortcut_specs
from .update_guard import plan_safe_update
from .windows_installer import build_windows_installer_scripts


def run_packaging_pipeline(root: Path, profile_id: str = "dashboard-full") -> dict[str, Any]:
    profiles = build_package_profile_report()
    profile_saved = write_package_profile_report(root)
    lock = write_dependency_lock(root, profile_id)
    manifest = write_package_manifest(root, profile_id)
    portable = build_portable_bundle(root, profile_id)
    installer = build_windows_installer_scripts(root, profile_id)
    shortcuts = generate_shortcut_specs()
    startup = installed_startup_health(root)
    update = plan_safe_update(active_live_session=True)
    migration = preview_package_migration()
    backup = create_package_backup(root)
    restore = restore_preview(root)
    rollback_point = create_rollback_point(root)
    rollback = rollback_preview(root)
    recovery_kit = build_offline_recovery_kit(root)
    safe_mode = package_safe_mode_status()
    verify = verify_package(root)
    evidence = export_package_evidence(root, {"profiles": profiles, "lock": lock, "manifest": manifest, "portable": portable, "installer": installer, "shortcuts": shortcuts, "startup": startup, "update": update, "migration": migration, "backup": backup, "restore": restore, "rollback_point": rollback_point, "rollback": rollback, "recovery_kit": recovery_kit, "safe_mode": safe_mode, "verify": verify})
    return {"status": "ok", "profiles": profiles, "profile_saved": profile_saved, "lock": lock, "manifest": manifest, "portable": portable, "installer": installer, "shortcuts": shortcuts, "startup": startup, "update": update, "migration": migration, "backup": backup, "restore": restore, "rollback_point": rollback_point, "rollback": rollback, "recovery_kit": recovery_kit, "safe_mode": safe_mode, "verify": verify, "evidence": evidence, "live_trading_enabled": False, "live_order_submitted": False}

