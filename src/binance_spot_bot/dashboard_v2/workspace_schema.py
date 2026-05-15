from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from binance_spot_bot.redaction import redact_text

SAFE_MODES = {"demo", "paper", "testnet-readiness", "all_safe_modes"}
REFRESH_POLICIES = {"manual", "snapshot", "realtime", "paused"}
MANDATORY_OPERATOR_WIDGETS = {"no_live_banner", "stop_button"}
UNSAFE_TEXT = re.compile(r"(?i)(<\s*script|javascript:|<\s*iframe|onerror\s*=|onload\s*=)")
ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{1,80}$")


@dataclass(frozen=True)
class DashboardWorkspaceMetadata:
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    updated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    owner: str = "local-operator"
    schema_version: int = 2


@dataclass(frozen=True)
class DashboardWorkspaceGrid:
    columns: int = 12
    row_height: int = 90
    gap: int = 12


@dataclass(frozen=True)
class DashboardWorkspaceWidget:
    widget_id: str
    widget_type: str
    title: str
    settings: dict[str, Any] = field(default_factory=dict)
    locked: bool = False
    safe_modes: tuple[str, ...] = ("demo", "paper", "testnet-readiness")
    data_sources: tuple[str, ...] = ("runtime_snapshot",)


@dataclass(frozen=True)
class DashboardWorkspacePanel:
    panel_id: str
    title: str
    x: int
    y: int
    w: int
    h: int
    widget_id: str
    min_w: int = 2
    min_h: int = 2
    pinned: bool = False
    collapsed: bool = False
    refresh_policy: str = "snapshot"
    query_scope: str = "runtime_snapshot"


@dataclass(frozen=True)
class DashboardWorkspaceLayout:
    grid: DashboardWorkspaceGrid = field(default_factory=DashboardWorkspaceGrid)
    panels: tuple[DashboardWorkspacePanel, ...] = field(default_factory=tuple)
    widgets: tuple[DashboardWorkspaceWidget, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DashboardWorkspace:
    workspace_id: str
    name: str
    description: str = ""
    version: str = "2.0"
    operator_level: str = "operator"
    mode_scope: str = "all_safe_modes"
    layout: DashboardWorkspaceLayout = field(default_factory=DashboardWorkspaceLayout)
    safety_widgets_locked: bool = True
    live_trading_enabled: bool = False
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    metadata: DashboardWorkspaceMetadata = field(default_factory=DashboardWorkspaceMetadata)


@dataclass(frozen=True)
class DashboardWorkspaceValidationResult:
    status: str
    blockers: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    live_trading_enabled: bool = False
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _unsafe_strings(value: Any, path: str = "value") -> list[str]:
    issues: list[str] = []
    if isinstance(value, str):
        if UNSAFE_TEXT.search(value):
            issues.append(f"{path} contains unsafe script/html content")
        if value != "[REDACTED]" and redact_text(value) != value:
            issues.append(f"{path} contains secret-like value")
    elif isinstance(value, dict):
        for key, item in value.items():
            if UNSAFE_TEXT.search(str(key)):
                issues.append(f"{path}.{key} contains unsafe key")
            issues.extend(_unsafe_strings(item, f"{path}.{key}"))
    elif isinstance(value, (list, tuple)):
        for idx, item in enumerate(value):
            issues.extend(_unsafe_strings(item, f"{path}[{idx}]"))
    return issues


def _validate_id(value: str, label: str) -> list[str]:
    return [] if ID_RE.match(value) else [f"{label} has invalid id"]


def validate_dashboard_workspace(workspace: DashboardWorkspace) -> DashboardWorkspaceValidationResult:
    blockers: list[str] = []
    warnings: list[str] = []
    blockers.extend(_validate_id(workspace.workspace_id, "workspace"))
    blockers.extend(_unsafe_strings(workspace.name, "workspace.name"))
    blockers.extend(_unsafe_strings(workspace.description, "workspace.description"))
    if workspace.live_trading_enabled:
        blockers.append("live_trading_enabled must be false")
    if workspace.mode_scope not in SAFE_MODES or workspace.mode_scope == "live":
        blockers.append("live mode scope is blocked")
    if not workspace.safety_widgets_locked:
        blockers.append("safety widgets must stay locked")
    if workspace.no_live_statement != dashboard_v2_no_live_statement():
        blockers.append("no-live statement missing or modified")
    if workspace.layout.grid.columns <= 0:
        blockers.append("grid columns must be positive")

    panel_ids: set[str] = set()
    widget_ids: set[str] = set()
    widget_types: set[str] = set()
    for widget in workspace.layout.widgets:
        blockers.extend(_validate_id(widget.widget_id, "widget"))
        if widget.widget_id in widget_ids:
            blockers.append(f"duplicate widget_id: {widget.widget_id}")
        widget_ids.add(widget.widget_id)
        widget_types.add(widget.widget_type)
        blockers.extend(_unsafe_strings(widget.title, f"widget.{widget.widget_id}.title"))
        blockers.extend(_unsafe_strings(widget.settings, f"widget.{widget.widget_id}.settings"))
        if widget.widget_type in MANDATORY_OPERATOR_WIDGETS and not widget.locked:
            blockers.append(f"safety widget must be locked: {widget.widget_type}")
        modes = set(_as_tuple(widget.safe_modes))
        if "live" in modes or not modes <= SAFE_MODES:
            blockers.append(f"widget {widget.widget_id} exposes unsafe mode")
        if widget.widget_type.startswith("live_") or ".live" in widget.widget_type:
            blockers.append(f"live widget type blocked: {widget.widget_type}")

    for panel in workspace.layout.panels:
        blockers.extend(_validate_id(panel.panel_id, "panel"))
        if panel.panel_id in panel_ids:
            blockers.append(f"duplicate panel_id: {panel.panel_id}")
        panel_ids.add(panel.panel_id)
        blockers.extend(_unsafe_strings(panel.title, f"panel.{panel.panel_id}.title"))
        if panel.widget_id not in widget_ids:
            blockers.append(f"panel references missing widget_id: {panel.widget_id}")
        if panel.w <= 0 or panel.h <= 0 or panel.min_w <= 0 or panel.min_h <= 0:
            blockers.append(f"panel {panel.panel_id} has invalid dimensions")
        if panel.refresh_policy not in REFRESH_POLICIES:
            blockers.append(f"unknown refresh_policy: {panel.refresh_policy}")

    if "no_live_banner" not in widget_types:
        blockers.append("missing no_live_banner widget")
    if workspace.operator_level == "operator":
        missing = MANDATORY_OPERATOR_WIDGETS - widget_types
        if missing:
            blockers.append(f"missing mandatory operator safety widgets: {', '.join(sorted(missing))}")
    if len(workspace.layout.panels) > 36:
        warnings.append("workspace has many panels")
    return DashboardWorkspaceValidationResult(
        status="ok" if not blockers else "blocked",
        blockers=tuple(blockers),
        warnings=tuple(warnings),
    )


def _widget_from_dict(payload: dict[str, Any]) -> DashboardWorkspaceWidget:
    return DashboardWorkspaceWidget(
        widget_id=str(payload["widget_id"]),
        widget_type=str(payload["widget_type"]),
        title=str(payload.get("title", payload["widget_type"])),
        settings=dict(payload.get("settings", {})),
        locked=bool(payload.get("locked", False)),
        safe_modes=_as_tuple(payload.get("safe_modes", ("demo", "paper", "testnet-readiness"))),
        data_sources=_as_tuple(payload.get("data_sources", ("runtime_snapshot",))),
    )


def _panel_from_dict(payload: dict[str, Any]) -> DashboardWorkspacePanel:
    return DashboardWorkspacePanel(
        panel_id=str(payload["panel_id"]),
        title=str(payload.get("title", payload["panel_id"])),
        x=int(payload.get("x", 0)),
        y=int(payload.get("y", 0)),
        w=int(payload.get("w", 4)),
        h=int(payload.get("h", 3)),
        widget_id=str(payload["widget_id"]),
        min_w=int(payload.get("min_w", 2)),
        min_h=int(payload.get("min_h", 2)),
        pinned=bool(payload.get("pinned", False)),
        collapsed=bool(payload.get("collapsed", False)),
        refresh_policy=str(payload.get("refresh_policy", "snapshot")),
        query_scope=str(payload.get("query_scope", "runtime_snapshot")),
    )


def dashboard_workspace_from_dict(payload: dict[str, Any]) -> DashboardWorkspace:
    layout = payload.get("layout", {})
    grid = layout.get("grid", {})
    metadata = payload.get("metadata", {})
    return DashboardWorkspace(
        workspace_id=str(payload["workspace_id"]),
        name=str(payload.get("name", "Workspace")),
        description=str(payload.get("description", "")),
        version=str(payload.get("version", "2.0")),
        operator_level=str(payload.get("operator_level", "operator")),
        mode_scope=str(payload.get("mode_scope", "all_safe_modes")),
        layout=DashboardWorkspaceLayout(
            grid=DashboardWorkspaceGrid(
                columns=int(grid.get("columns", 12)),
                row_height=int(grid.get("row_height", 90)),
                gap=int(grid.get("gap", 12)),
            ),
            panels=tuple(_panel_from_dict(item) for item in layout.get("panels", [])),
            widgets=tuple(_widget_from_dict(item) for item in layout.get("widgets", [])),
        ),
        safety_widgets_locked=bool(payload.get("safety_widgets_locked", True)),
        live_trading_enabled=bool(payload.get("live_trading_enabled", False)),
        no_live_statement=str(payload.get("no_live_statement", dashboard_v2_no_live_statement())),
        metadata=DashboardWorkspaceMetadata(
            created_at_ms=int(metadata.get("created_at_ms", int(time.time() * 1000))),
            updated_at_ms=int(metadata.get("updated_at_ms", int(time.time() * 1000))),
            owner=str(metadata.get("owner", "local-operator")),
            schema_version=int(metadata.get("schema_version", 2)),
        ),
    )


def dashboard_workspace_to_dict(workspace: DashboardWorkspace, *, redact: bool = True) -> dict[str, Any]:
    payload = asdict(workspace)
    return redact_dashboard_payload(payload) if redact else payload


def load_dashboard_workspace(path: Path) -> DashboardWorkspace:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return dashboard_workspace_from_dict(payload)


def write_dashboard_workspace(path: Path, workspace: DashboardWorkspace) -> Path:
    result = validate_dashboard_workspace(workspace)
    if result.status != "ok":
        raise ValueError("; ".join(result.blockers))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dashboard_workspace_to_dict(workspace), indent=2, default=str), encoding="utf-8")
    return path
