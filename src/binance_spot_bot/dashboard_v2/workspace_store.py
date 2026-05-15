from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .widget_registry import validate_widget_types
from .workspace_schema import (
    DashboardWorkspace,
    dashboard_workspace_from_dict,
    dashboard_workspace_to_dict,
    load_dashboard_workspace,
    validate_dashboard_workspace,
    write_dashboard_workspace,
)

SAFE_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{1,80}$")


def _hash_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


class DashboardWorkspaceStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.layouts_dir = self.root / "layouts"
        self.exports_dir = self.root / "exports"
        self.reports_dir = self.root / "reports"
        self.evidence_dir = self.root / "evidence"

    def ensure(self) -> None:
        for path in (self.layouts_dir, self.exports_dir, self.reports_dir, self.evidence_dir):
            path.mkdir(parents=True, exist_ok=True)

    def _safe_workspace_path(self, workspace_id: str) -> Path:
        if not SAFE_ID.match(workspace_id):
            raise ValueError("unsafe workspace id")
        self.ensure()
        path = (self.layouts_dir / f"{workspace_id}.json").resolve()
        if self.layouts_dir.resolve() not in path.parents:
            raise ValueError("unsafe workspace path")
        return path

    def save(self, workspace: DashboardWorkspace) -> dict[str, Any]:
        self.ensure()
        path = self._safe_workspace_path(workspace.workspace_id)
        write_dashboard_workspace(path, workspace)
        payload = dashboard_workspace_to_dict(workspace)
        manifest = {"workspace_id": workspace.workspace_id, "path": str(path), "sha256": _hash_payload(payload), "updated_at_ms": int(time.time() * 1000)}
        (path.with_suffix(".manifest.json")).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return redact_dashboard_payload({"status": "ok", "workspace": payload, "manifest": manifest, "live_trading_enabled": False})

    def load(self, workspace_id: str) -> DashboardWorkspace:
        return load_dashboard_workspace(self._safe_workspace_path(workspace_id))

    def list(self) -> dict[str, Any]:
        self.ensure()
        rows = []
        for path in sorted(self.layouts_dir.glob("*.json")):
            if path.name.endswith(".manifest.json"):
                continue
            try:
                workspace = load_dashboard_workspace(path)
                rows.append(
                    {
                        "workspace_id": workspace.workspace_id,
                        "name": workspace.name,
                        "description": workspace.description,
                        "validation": validate_dashboard_workspace(workspace).to_dict(),
                    }
                )
            except Exception as exc:
                rows.append({"workspace_id": path.stem, "status": "blocked", "error": str(exc)})
        return {"status": "ok", "workspaces": rows, "count": len(rows), "live_trading_enabled": False}

    def delete(self, workspace_id: str, *, confirm: str = "") -> dict[str, Any]:
        if confirm != workspace_id:
            return {"status": "blocked", "blockers": ["delete requires confirm matching workspace id"], "live_trading_enabled": False}
        path = self._safe_workspace_path(workspace_id)
        if path.exists():
            path.unlink()
        manifest = path.with_suffix(".manifest.json")
        if manifest.exists():
            manifest.unlink()
        return {"status": "ok", "deleted": workspace_id, "live_trading_enabled": False}

    def clone(self, workspace_id: str, *, name: str = "") -> dict[str, Any]:
        source = dashboard_workspace_to_dict(self.load(workspace_id))
        clone_id = f"{workspace_id}-clone-{int(time.time() * 1000)}"
        source["workspace_id"] = clone_id
        source["name"] = name or f"{source.get('name', workspace_id)} Clone"
        clone = dashboard_workspace_from_dict(source)
        return self.save(clone)

    def export(self, workspace_id: str) -> dict[str, Any]:
        self.ensure()
        workspace = self.load(workspace_id)
        payload = dashboard_workspace_to_dict(workspace)
        path = self.exports_dir / f"{workspace_id}-export.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        summary = self.exports_dir / f"{workspace_id}-export.md"
        summary.write_text(
            f"# Dashboard V2 Workspace Export\n\nWorkspace: {workspace.name}\n\nNo-live proof: {dashboard_v2_no_live_statement()}\n",
            encoding="utf-8",
        )
        return {"status": "ok", "path": str(path), "summary": str(summary), "sha256": _hash_payload(payload), "live_trading_enabled": False}

    def import_workspace(self, path: Path, *, dry_run: bool = False) -> dict[str, Any]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        redacted = redact_dashboard_payload(raw)
        workspace = dashboard_workspace_from_dict(redacted)
        schema_result = validate_dashboard_workspace(workspace)
        widget_result = validate_widget_types([widget.widget_type for widget in workspace.layout.widgets])
        blockers = list(schema_result.blockers) + list(widget_result["blockers"])
        if blockers:
            return {"status": "blocked", "blockers": blockers, "live_trading_enabled": False}
        preview = {"workspace_id": workspace.workspace_id, "name": workspace.name, "widgets": len(workspace.layout.widgets), "panels": len(workspace.layout.panels)}
        if dry_run:
            return {"status": "ok", "dry_run": True, "preview": preview, "live_trading_enabled": False}
        saved = self.save(workspace)
        return {"status": "ok", "dry_run": False, "preview": preview, "saved": saved, "live_trading_enabled": False}

    def verify_hashes(self) -> dict[str, Any]:
        blockers: list[str] = []
        checked = 0
        for path in sorted(self.layouts_dir.glob("*.json")):
            if path.name.endswith(".manifest.json"):
                continue
            manifest_path = path.with_suffix(".manifest.json")
            if not manifest_path.exists():
                blockers.append(f"missing manifest: {path.name}")
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            checked += 1
            if manifest.get("sha256") != _hash_payload(payload):
                blockers.append(f"hash mismatch: {path.name}")
        return {"status": "ok" if not blockers else "blocked", "checked": checked, "blockers": blockers, "live_trading_enabled": False}


def default_workspace_store(root: Path | str = ".") -> DashboardWorkspaceStore:
    return DashboardWorkspaceStore(Path(root) / "data" / "dashboard-v2" / "workspaces")
