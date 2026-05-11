from .safety import LiveSafetyDecision, no_live_order
def live_session_manager(level: int): return {**LiveSafetyDecision("ready", "manage_session", [f"level_{level}"]).to_dict(), **no_live_order()}
