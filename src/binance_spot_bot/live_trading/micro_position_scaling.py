from .safety import LiveSafetyDecision, no_live_order
def micro_position_scaling(current: int, target: int, approved: bool): return {**LiveSafetyDecision("blocked" if target > current + 1 or not approved else "approved", "scale_review", ["no_level_skip"] if target > current + 1 else []).to_dict(), **no_live_order()}
