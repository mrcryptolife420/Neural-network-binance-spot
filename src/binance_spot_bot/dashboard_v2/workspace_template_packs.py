from __future__ import annotations

from typing import Any

from .extension_pack_schema import (
    DashboardExtensionPack,
    DashboardExtensionPackManifest,
    DashboardPackContent,
    finalized_extension_pack,
    validate_dashboard_extension_pack,
)
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .workspace_presets import build_workspace_preset
from .workspace_schema import dashboard_workspace_to_dict


TEMPLATE_PACKS: dict[str, tuple[str, str, str]] = {
    "beginner_paper_operator": ("Beginner Paper Operator", "workspace_template", "paper_session_trader"),
    "demo_spot_control_room": ("Demo Spot Trading Control Room", "workspace_template", "demo_spot_monitor"),
    "market_analysis_desk": ("Binance Spot Market Scanner", "workspace_template", "market_analysis"),
    "risk_alerts_war_room": ("Risk & Alerts War Room", "workspace_template", "operator_overview"),
    "model_monitoring_desk": ("Model Monitoring Desk", "model_ops_pack", "model_ops"),
    "portfolio_allocation_desk": ("Portfolio Allocation Desk", "portfolio_ops_pack", "portfolio_ops"),
    "support_evidence_desk": ("Support & Evidence Desk", "support_evidence_pack", "support_evidence"),
    "release_roadmap_ops_desk": ("Roadmap/Release Ops Desk", "release_ops_pack", "support_evidence"),
    "uat_training_desk": ("UAT Training Desk", "training_uat_pack", "operator_overview"),
}


def build_template_pack(pack_id: str) -> DashboardExtensionPack:
    if pack_id not in TEMPLATE_PACKS:
        raise ValueError(f"unknown template pack: {pack_id}")
    name, pack_type, preset = TEMPLATE_PACKS[pack_id]
    workspace = build_workspace_preset(preset, name=name)
    required = tuple(sorted({widget.widget_type for widget in workspace.layout.widgets}))
    pack = DashboardExtensionPack(
        manifest=DashboardExtensionPackManifest(
            pack_id=pack_id,
            name=name,
            description=f"Local pluginless Dashboard V2 pack for {name}.",
            version="1.0",
            pack_type=pack_type,
            required_widget_types=required,
            tags=(preset, "local-only", "no-live"),
        ),
        content=DashboardPackContent(
            workspace_templates=(dashboard_workspace_to_dict(workspace),),
            docs=f"# {name}\n\n{dashboard_v2_no_live_statement()}\n",
            evidence_expectations={"workspace_validation": True, "no_live_proof": True},
        ),
    )
    return finalized_extension_pack(pack)


def builtin_template_pack_catalog() -> list[DashboardExtensionPack]:
    return [build_template_pack(pack_id) for pack_id in sorted(TEMPLATE_PACKS)]


def template_packs_payload() -> dict[str, Any]:
    packs = builtin_template_pack_catalog()
    return redact_dashboard_payload(
        {
            "status": "ok",
            "packs": [
                {
                    "pack_id": pack.manifest.pack_id,
                    "name": pack.manifest.name,
                    "pack_type": pack.manifest.pack_type,
                    "validation": validate_dashboard_extension_pack(pack).to_dict(),
                }
                for pack in packs
            ],
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )
