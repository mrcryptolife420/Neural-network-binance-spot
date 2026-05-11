from .safety import LiveSafetyDecision, no_live_order
def live_monitoring(heartbeat_ok: bool): return {**LiveSafetyDecision("ok" if heartbeat_ok else "blocked", "monitor", [] if heartbeat_ok else ["heartbeat_failed"], requires_approval=False).to_dict(), **no_live_order()}
