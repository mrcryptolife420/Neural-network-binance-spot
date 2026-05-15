from __future__ import annotations

from typing import Any

from .schemas import DashboardV2ActionRequest, DashboardV2ActionResult, SUPPORTED_MODES

READ_ONLY = {"health", "config", "pages", "snapshot", "operator-health", "no-live-proof"}
RUNTIME = {"runtime.start", "runtime.pause", "runtime.stop", "runtime.step", "runtime.reset"}
EVIDENCE = {"evidence.operator-export", "support-bundle.create"}
DEMO_GUARDED = {"demo.order.preview", "demo.order.test", "demo.order.place"}


def evaluate_dashboard_v2_action(request: DashboardV2ActionRequest, *, demo_armed: bool = False) -> DashboardV2ActionResult:
    action = request.action
    if request.mode not in SUPPORTED_MODES:
        return DashboardV2ActionResult("blocked", action, "unsupported or live mode is not allowed")
    lowered = action.lower()
    if any(term in lowered for term in ("live", "withdraw", "real-order", "account")):
        return DashboardV2ActionResult("blocked", action, "forbidden live/account/order action")
    if action in READ_ONLY | RUNTIME | EVIDENCE:
        return DashboardV2ActionResult("ok", action, payload={"mode": request.mode})
    if action in DEMO_GUARDED:
        if request.mode != "demo":
            return DashboardV2ActionResult("blocked", action, "demo order actions require demo mode")
        if action == "demo.order.place" and (not demo_armed or request.confirm != "CONFIRM_DEMO_ORDER"):
            return DashboardV2ActionResult("blocked", action, "guarded demo order requires armed demo and confirm phrase")
        return DashboardV2ActionResult("ok", action, payload={"guarded": action == "demo.order.place"})
    return DashboardV2ActionResult("blocked", action, "action is not allowlisted")


def dashboard_v2_action_matrix() -> dict[str, Any]:
    rows = [evaluate_dashboard_v2_action(DashboardV2ActionRequest(action=action)).to_dict() for action in sorted(READ_ONLY | RUNTIME | EVIDENCE)]
    rows.append(evaluate_dashboard_v2_action(DashboardV2ActionRequest(action="live.order.place", mode="live")).to_dict())
    return {"status": "ok", "actions": rows, "live_trading_enabled": False}
