from __future__ import annotations

from typing import Any

DRILLS = ("disarm", "emergency_stop", "cancel_pending_order_fake", "reconciliation_mismatch", "dashboard_disconnect", "stale_data", "evidence_writer_failure", "profile_rollback", "risk_preset_rollback", "live_profile_demotion")


def run_rollback_drill(drill: str = "disarm") -> dict[str, Any]:
    status = "passed" if drill in DRILLS else "failed"
    return {
        "status": status,
        "drill": drill,
        "mode": "offline_fake",
        "actions_taken": ["fake_disarm_signal", "evidence_snapshot"],
        "blockers": [] if status == "passed" else ["unknown_drill"],
        "recommended_fixes": [] if status == "passed" else ["register_drill"],
        "live_order_submitted": False,
        "live_rearmed": False,
    }

