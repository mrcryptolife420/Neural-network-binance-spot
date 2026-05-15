from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


def recommend_extension_packs(context: dict[str, Any] | None = None) -> dict[str, Any]:
    context = context or {}
    workflow = str(context.get("workflow", "paper-session"))
    if "demo" in workflow:
        template = "demo_spot_control_room"
        analytics = ["market_analytics", "operator_analytics"]
        watchlist = "operator_demo_watchlist"
    elif "model" in workflow:
        template = "model_monitoring_desk"
        analytics = ["model_analytics"]
        watchlist = "binance_spot_majors"
    elif "portfolio" in workflow:
        template = "portfolio_allocation_desk"
        analytics = ["portfolio_analytics"]
        watchlist = "binance_spot_majors"
    elif "support" in workflow:
        template = "support_evidence_desk"
        analytics = ["operator_analytics"]
        watchlist = "low_scope_smoke_watchlist"
    else:
        template = "beginner_paper_operator"
        analytics = ["paper_trading_analytics"]
        watchlist = "operator_demo_watchlist"
    return redact_dashboard_payload(
        {
            "status": "ok",
            "workflow": workflow,
            "recommended_template_pack": template,
            "recommended_analytics_presets": analytics,
            "recommended_watchlist": watchlist,
            "reasons": ["matches safe local workflow", "uses built-in no-live template"],
            "blockers": [],
            "expected_impact": "faster local workspace setup",
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )


def write_pack_recommendations(root: Path | str = ".", workflow: str = "paper-session") -> dict[str, Any]:
    out = Path(root) / "data" / "dashboard-v2" / "extension-packs" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    payload = recommend_extension_packs({"workflow": workflow})
    json_path = out / "pack-recommendations.json"
    md_path = out / "pack-recommendations.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(f"# Pack Recommendations\n\nWorkflow: {workflow}\n\nTemplate: {payload['recommended_template_pack']}\n", encoding="utf-8")
    return {"status": "ok", "json": str(json_path), "markdown": str(md_path), "report": payload, "live_trading_enabled": False}
