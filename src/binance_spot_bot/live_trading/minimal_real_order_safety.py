from .safety import LiveSafetyDecision, block_without_confirmation, no_live_order
def minimal_real_order_safety(confirm: str): return {**LiveSafetyDecision("blocked" if block_without_confirmation(confirm, "I_ACCEPT_MICRO_LIVE_ORDER_RISK") else "armed", "manual_review", ["micro_order_gated"]).to_dict(), **no_live_order()}
