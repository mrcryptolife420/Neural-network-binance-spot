from __future__ import annotations

from .safety import LiveSafetyDecision, no_live_order


def live_monitoring(heartbeat_ok: bool):
    return {**LiveSafetyDecision("ok" if heartbeat_ok else "blocked", "monitor", [] if heartbeat_ok else ["heartbeat_failed"], requires_approval=False).to_dict(), **no_live_order()}


def live_monitoring_heartbeat(*, backend_alive: bool = True, market_data_fresh: bool = True, spread_ok: bool = True, reconciliation_ok: bool = True, kill_switch: bool = False) -> dict[str, object]:
    blockers = []
    if not backend_alive:
        blockers.append("backend heartbeat failed")
    if not market_data_fresh:
        blockers.append("market data stale")
    if not spread_ok:
        blockers.append("spread too high")
    if not reconciliation_ok:
        blockers.append("reconciliation failed")
    if kill_switch:
        blockers.append("kill switch active")
    status = "disarm_required" if blockers else "healthy"
    return {"status": status, "blockers": blockers, "disarm_required": bool(blockers), "live_trading_enabled": False}
