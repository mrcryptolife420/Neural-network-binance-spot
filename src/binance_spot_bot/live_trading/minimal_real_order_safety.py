from . import REAL_ORDER_CONFIRM
from .safety import LiveSafetyDecision, block_without_confirmation, no_live_order


def minimal_real_order_safety(confirm: str):
    blocked = block_without_confirmation(confirm, REAL_ORDER_CONFIRM)
    return {**LiveSafetyDecision("blocked" if blocked else "armed", "manual_review", ["micro_order_gated"]).to_dict(), "live_order_placement_enabled": False, **no_live_order()}
