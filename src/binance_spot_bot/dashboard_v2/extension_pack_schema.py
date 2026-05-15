from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_text

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .widget_registry import validate_widget_types
from .workspace_schema import dashboard_workspace_from_dict, validate_dashboard_workspace

PACK_TYPES = {
    "workspace_template",
    "widget_preset",
    "analytics_preset",
    "watchlist_pack",
    "operator_workflow",
    "support_evidence_pack",
    "model_ops_pack",
    "portfolio_ops_pack",
    "training_uat_pack",
    "release_ops_pack",
}
SAFE_SCHEMA_VERSIONS = {2}
UNSAFE_TEXT = re.compile(r"(?i)(<\s*script|javascript:|<\s*iframe|onerror\s*=|onload\s*=)")
REMOTE_URL = re.compile(r"(?i)\bhttps?://")
CODE_KEYS = {"code", "script", "eval", "function_body", "python", "javascript", "js", "py"}


@dataclass(frozen=True)
class DashboardPackDependency:
    pack_id: str
    version: str = ">=1.0"


@dataclass(frozen=True)
class DashboardPackCompatibility:
    workspace_schema_versions: tuple[int, ...] = (2,)
    dashboard_v2_features: tuple[str, ...] = ("workspaces", "widget_registry", "analytics_query")
    safe_modes: tuple[str, ...] = ("demo", "paper", "testnet-readiness")


@dataclass(frozen=True)
class DashboardExtensionPackManifest:
    pack_id: str
    name: str
    description: str
    version: str
    pack_type: str
    schema_version: int = 2
    author: str = "local"
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    compatible_workspace_schema_versions: tuple[int, ...] = (2,)
    required_widget_types: tuple[str, ...] = ("no_live_banner", "stop_button")
    required_dashboard_v2_features: tuple[str, ...] = ("workspaces", "widget_registry")
    mode_scope: str = "all_safe_modes"
    operator_level: str = "operator"
    tags: tuple[str, ...] = ()
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False
    content_hash: str = ""


@dataclass(frozen=True)
class DashboardPackContent:
    workspace_templates: tuple[dict[str, Any], ...] = ()
    widget_presets: tuple[dict[str, Any], ...] = ()
    analytics_presets: tuple[dict[str, Any], ...] = ()
    watchlists: tuple[dict[str, Any], ...] = ()
    workflow_steps: tuple[dict[str, Any], ...] = ()
    docs: str = ""
    evidence_expectations: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DashboardExtensionPack:
    manifest: DashboardExtensionPackManifest
    content: DashboardPackContent = field(default_factory=DashboardPackContent)
    dependencies: tuple[DashboardPackDependency, ...] = ()
    compatibility: DashboardPackCompatibility = field(default_factory=DashboardPackCompatibility)


@dataclass(frozen=True)
class DashboardPackValidationResult:
    status: str
    blockers: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    no_live_statement: str = field(default_factory=dashboard_v2_no_live_statement)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def compute_pack_content_hash(content: DashboardPackContent | dict[str, Any]) -> str:
    payload = asdict(content) if isinstance(content, DashboardPackContent) else content
    text = json.dumps(redact_dashboard_payload(payload), sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    return (value,)


def _scan_unsafe(value: Any, path: str = "pack") -> list[str]:
    issues: list[str] = []
    if isinstance(value, str):
        if UNSAFE_TEXT.search(value):
            issues.append(f"{path} contains unsafe script/html content")
        if REMOTE_URL.search(value):
            issues.append(f"{path} contains remote URL")
        if value != "[REDACTED]" and redact_text(value) != value:
            issues.append(f"{path} contains secret-like value")
    elif isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            if key_text.lower() in CODE_KEYS:
                issues.append(f"{path}.{key_text} contains code execution field")
            if UNSAFE_TEXT.search(key_text):
                issues.append(f"{path}.{key_text} contains unsafe key")
            issues.extend(_scan_unsafe(item, f"{path}.{key_text}"))
    elif isinstance(value, (list, tuple)):
        for idx, item in enumerate(value):
            issues.extend(_scan_unsafe(item, f"{path}[{idx}]"))
    return issues


def dashboard_extension_pack_to_dict(pack: DashboardExtensionPack, *, redact: bool = True) -> dict[str, Any]:
    payload = asdict(pack)
    return redact_dashboard_payload(payload) if redact else payload


def dashboard_extension_pack_from_dict(payload: dict[str, Any]) -> DashboardExtensionPack:
    manifest = payload.get("manifest", {})
    content = payload.get("content", {})
    return DashboardExtensionPack(
        manifest=DashboardExtensionPackManifest(
            pack_id=str(manifest["pack_id"]),
            name=str(manifest.get("name", manifest["pack_id"])),
            description=str(manifest.get("description", "")),
            version=str(manifest.get("version", "1.0")),
            pack_type=str(manifest.get("pack_type", "workspace_template")),
            schema_version=int(manifest.get("schema_version", 2)),
            author=str(manifest.get("author", "local")),
            created_at_ms=int(manifest.get("created_at_ms", int(time.time() * 1000))),
            compatible_workspace_schema_versions=tuple(int(item) for item in _tuple(manifest.get("compatible_workspace_schema_versions", (2,)))),
            required_widget_types=tuple(str(item) for item in _tuple(manifest.get("required_widget_types", ("no_live_banner", "stop_button")))),
            required_dashboard_v2_features=tuple(str(item) for item in _tuple(manifest.get("required_dashboard_v2_features", ("workspaces", "widget_registry")))),
            mode_scope=str(manifest.get("mode_scope", "all_safe_modes")),
            operator_level=str(manifest.get("operator_level", "operator")),
            tags=tuple(str(item) for item in _tuple(manifest.get("tags", ()))),
            no_live_statement=str(manifest.get("no_live_statement", dashboard_v2_no_live_statement())),
            live_trading_enabled=bool(manifest.get("live_trading_enabled", False)),
            content_hash=str(manifest.get("content_hash", "")),
        ),
        content=DashboardPackContent(
            workspace_templates=tuple(dict(item) for item in content.get("workspace_templates", [])),
            widget_presets=tuple(dict(item) for item in content.get("widget_presets", [])),
            analytics_presets=tuple(dict(item) for item in content.get("analytics_presets", [])),
            watchlists=tuple(dict(item) for item in content.get("watchlists", [])),
            workflow_steps=tuple(dict(item) for item in content.get("workflow_steps", [])),
            docs=str(content.get("docs", "")),
            evidence_expectations=dict(content.get("evidence_expectations", {})),
        ),
        dependencies=tuple(DashboardPackDependency(str(item["pack_id"]), str(item.get("version", ">=1.0"))) for item in payload.get("dependencies", [])),
        compatibility=DashboardPackCompatibility(
            workspace_schema_versions=tuple(int(item) for item in _tuple(payload.get("compatibility", {}).get("workspace_schema_versions", (2,)))),
            dashboard_v2_features=tuple(str(item) for item in _tuple(payload.get("compatibility", {}).get("dashboard_v2_features", ("workspaces", "widget_registry")))),
            safe_modes=tuple(str(item) for item in _tuple(payload.get("compatibility", {}).get("safe_modes", ("demo", "paper", "testnet-readiness")))),
        ),
    )


def validate_dashboard_extension_pack(pack: DashboardExtensionPack) -> DashboardPackValidationResult:
    blockers: list[str] = []
    warnings: list[str] = []
    manifest = pack.manifest
    if manifest.pack_type not in PACK_TYPES:
        blockers.append(f"unknown pack_type: {manifest.pack_type}")
    if manifest.live_trading_enabled:
        blockers.append("live_trading_enabled must be false")
    if manifest.mode_scope == "live" or "live" in manifest.mode_scope:
        blockers.append("live mode is blocked")
    if manifest.no_live_statement != dashboard_v2_no_live_statement():
        blockers.append("missing no-live statement")
    if not manifest.required_widget_types:
        blockers.append("required widget types cannot be empty")
    blockers.extend(validate_widget_types(manifest.required_widget_types)["blockers"])
    unsupported_versions = set(manifest.compatible_workspace_schema_versions) - SAFE_SCHEMA_VERSIONS
    if unsupported_versions:
        blockers.append(f"unsupported workspace schema versions: {sorted(unsupported_versions)}")
    if pack.compatibility.safe_modes and ("live" in pack.compatibility.safe_modes or not set(pack.compatibility.safe_modes) <= {"demo", "paper", "testnet-readiness"}):
        blockers.append("compatibility exposes unsafe mode")
    expected_hash = compute_pack_content_hash(pack.content)
    if manifest.content_hash and manifest.content_hash != expected_hash:
        blockers.append("content hash mismatch")
    blockers.extend(_scan_unsafe(dashboard_extension_pack_to_dict(pack, redact=False), "pack"))
    for template in pack.content.workspace_templates:
        try:
            workspace = dashboard_workspace_from_dict(redact_dashboard_payload(template))
            result = validate_dashboard_workspace(workspace)
            blockers.extend(f"workspace_template.{workspace.workspace_id}: {item}" for item in result.blockers)
        except Exception as exc:
            blockers.append(f"invalid workspace template: {exc}")
    return DashboardPackValidationResult(status="ok" if not blockers else "blocked", blockers=tuple(blockers), warnings=tuple(warnings))


def finalized_extension_pack(pack: DashboardExtensionPack) -> DashboardExtensionPack:
    payload = dashboard_extension_pack_to_dict(pack, redact=True)
    payload["manifest"]["content_hash"] = compute_pack_content_hash(payload["content"])
    return dashboard_extension_pack_from_dict(payload)


def load_dashboard_extension_pack(path: Path) -> DashboardExtensionPack:
    return dashboard_extension_pack_from_dict(redact_dashboard_payload(json.loads(path.read_text(encoding="utf-8"))))


def write_dashboard_extension_pack(path: Path, pack: DashboardExtensionPack) -> Path:
    pack = finalized_extension_pack(pack)
    result = validate_dashboard_extension_pack(pack)
    if result.status != "ok":
        raise ValueError("; ".join(result.blockers))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dashboard_extension_pack_to_dict(pack), indent=2, default=str), encoding="utf-8")
    return path
