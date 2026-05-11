from .safety import LiveSafetyDecision, no_live_order, preview_hash
def live_order_preview(intent: dict): return {**LiveSafetyDecision("preview", "no_submit", ["operator_approval_required"]).to_dict(), "preview_hash": preview_hash(intent), **no_live_order()}
