from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .extension_pack_schema import (
    DashboardExtensionPack,
    dashboard_extension_pack_to_dict,
    load_dashboard_extension_pack,
    validate_dashboard_extension_pack,
    write_dashboard_extension_pack,
)
from .pack_compatibility import evaluate_pack_compatibility
from .pack_install_preview import preview_pack_install
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .workspace_template_packs import builtin_template_pack_catalog, build_template_pack

SAFE_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{1,80}$")


class DashboardExtensionPackRegistry:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.installed_dir = self.root / "installed"
        self.catalog_dir = self.root / "catalog"
        self.exports_dir = self.root / "exports"
        self.evidence_dir = self.root / "evidence"

    def ensure(self) -> None:
        for path in (self.installed_dir, self.catalog_dir, self.exports_dir, self.evidence_dir):
            path.mkdir(parents=True, exist_ok=True)

    def _path(self, pack_id: str, folder: Path) -> Path:
        if not SAFE_ID.match(pack_id):
            raise ValueError("unsafe pack id")
        self.ensure()
        path = (folder / f"{pack_id}.json").resolve()
        if folder.resolve() not in path.parents:
            raise ValueError("unsafe pack path")
        return path

    def generate_catalog(self) -> dict[str, Any]:
        self.ensure()
        rows = []
        for pack in builtin_template_pack_catalog():
            path = self._path(pack.manifest.pack_id, self.catalog_dir)
            write_dashboard_extension_pack(path, pack)
            rows.append({"pack_id": pack.manifest.pack_id, "name": pack.manifest.name, "path": str(path)})
        return {"status": "ok", "catalog": rows, "live_trading_enabled": False}

    def available(self) -> dict[str, Any]:
        self.generate_catalog()
        rows = [dashboard_extension_pack_to_dict(load_dashboard_extension_pack(path))["manifest"] for path in sorted(self.catalog_dir.glob("*.json"))]
        return {"status": "ok", "packs": rows, "count": len(rows), "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}

    def installed(self) -> dict[str, Any]:
        self.ensure()
        rows = [dashboard_extension_pack_to_dict(load_dashboard_extension_pack(path))["manifest"] for path in sorted(self.installed_dir.glob("*.json")) if not path.name.endswith(".state.json")]
        return {"status": "ok", "packs": rows, "count": len(rows), "live_trading_enabled": False}

    def load_pack(self, pack_id: str) -> DashboardExtensionPack:
        installed = self._path(pack_id, self.installed_dir)
        if installed.exists():
            return load_dashboard_extension_pack(installed)
        catalog = self._path(pack_id, self.catalog_dir)
        if catalog.exists():
            return load_dashboard_extension_pack(catalog)
        return build_template_pack(pack_id)

    def install(self, pack: DashboardExtensionPack, *, confirm: str = "", enabled: bool = False) -> dict[str, Any]:
        preview = preview_pack_install(pack)
        if preview["status"] != "ok":
            return preview
        if confirm != "INSTALL_LOCAL_PACK":
            return {"status": "blocked", "blockers": ["install requires confirm INSTALL_LOCAL_PACK"], "preview": preview, "live_trading_enabled": False}
        path = self._path(pack.manifest.pack_id, self.installed_dir)
        write_dashboard_extension_pack(path, pack)
        state_path = path.with_suffix(".state.json")
        state_path.write_text(json.dumps({"enabled": enabled, "live_trading_enabled": False}, indent=2), encoding="utf-8")
        return {"status": "ok", "path": str(path), "enabled": enabled, "preview": preview, "live_trading_enabled": False}

    def install_file(self, path: Path, *, confirm: str = "", enabled: bool = False) -> dict[str, Any]:
        return self.install(load_dashboard_extension_pack(path), confirm=confirm, enabled=enabled)

    def uninstall(self, pack_id: str, *, confirm: str = "") -> dict[str, Any]:
        if confirm != "UNINSTALL_LOCAL_PACK":
            return {"status": "blocked", "blockers": ["uninstall requires confirm UNINSTALL_LOCAL_PACK"], "live_trading_enabled": False}
        path = self._path(pack_id, self.installed_dir)
        if path.exists():
            path.unlink()
        state = path.with_suffix(".state.json")
        if state.exists():
            state.unlink()
        return {"status": "ok", "pack_id": pack_id, "live_trading_enabled": False}

    def set_enabled(self, pack_id: str, enabled: bool) -> dict[str, Any]:
        path = self._path(pack_id, self.installed_dir)
        if not path.exists():
            return {"status": "blocked", "blockers": ["pack is not installed"], "live_trading_enabled": False}
        path.with_suffix(".state.json").write_text(json.dumps({"enabled": enabled, "live_trading_enabled": False}, indent=2), encoding="utf-8")
        return {"status": "ok", "pack_id": pack_id, "enabled": enabled, "live_trading_enabled": False}

    def validate_installed(self) -> dict[str, Any]:
        rows = []
        blockers = []
        for path in sorted(self.installed_dir.glob("*.json")):
            if path.name.endswith(".state.json"):
                continue
            pack = load_dashboard_extension_pack(path)
            validation = validate_dashboard_extension_pack(pack).to_dict()
            compatibility = evaluate_pack_compatibility(pack)
            rows.append({"pack_id": pack.manifest.pack_id, "validation": validation, "compatibility": compatibility})
            blockers.extend(validation["blockers"])
            blockers.extend(compatibility["blockers"])
        return {"status": "ok" if not blockers else "blocked", "installed": rows, "blockers": blockers, "live_trading_enabled": False}

    def export(self, pack_id: str) -> dict[str, Any]:
        pack = self.load_pack(pack_id)
        path = self._path(pack_id, self.exports_dir)
        write_dashboard_extension_pack(path, pack)
        return {"status": "ok", "path": str(path), "pack_id": pack_id, "live_trading_enabled": False}


def default_extension_pack_registry(root: Path | str = ".") -> DashboardExtensionPackRegistry:
    return DashboardExtensionPackRegistry(Path(root) / "data" / "dashboard-v2" / "extension-packs")
