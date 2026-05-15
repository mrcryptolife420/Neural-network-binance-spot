from __future__ import annotations

from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload

SAFE_COMMANDS = {
    "validate-config",
    "preflight",
    "dashboard-v2-smoke",
    "dashboard-v2-no-live-proof",
    "dashboard-v2-workspace-presets",
    "dashboard-v2-widget-registry",
    "dashboard-v2-extension-packs",
    "dashboard-v2-extension-pack-evidence-export",
    "support-bundle",
    "operator-quality-gate",
}

WORKFLOW_PACKS: dict[str, list[dict[str, Any]]] = {
    "first_install_health_check": [{"step": "Validate config", "command": "validate-config"}, {"step": "Run preflight", "command": "preflight"}],
    "first_dashboard_launch": [{"step": "Smoke Dashboard V2", "command": "dashboard-v2-smoke"}],
    "first_paper_session": [{"step": "Open paper workspace", "command": "dashboard-v2-workspace-presets"}],
    "demo_spot_guarded_order_rehearsal": [{"step": "Review no-live proof", "command": "dashboard-v2-no-live-proof"}],
    "support_bundle_creation": [{"step": "Create support bundle", "command": "support-bundle"}],
    "evidence_review": [{"step": "Export pack evidence", "command": "dashboard-v2-extension-pack-evidence-export"}],
    "release_readiness_review": [{"step": "Operator quality gate", "command": "operator-quality-gate"}],
}


def workflow_packs_payload() -> dict[str, Any]:
    rows = []
    for workflow_id, steps in sorted(WORKFLOW_PACKS.items()):
        blockers = [f"unsafe command: {step['command']}" for step in steps if step["command"] not in SAFE_COMMANDS]
        rows.append({"workflow_id": workflow_id, "steps": steps, "status": "ok" if not blockers else "blocked", "blockers": blockers})
    return redact_dashboard_payload({"status": "ok", "workflow_packs": rows, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False})
