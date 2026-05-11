from .safety import LiveSafetyDecision, no_live_order
def live_session_review(evidence_present: bool, unknown_order_state: bool = False): return {**LiveSafetyDecision("blocked" if not evidence_present or unknown_order_state else "ok", "review", [r for r, flag in {"missing_evidence": not evidence_present, "unknown_order_state": unknown_order_state}.items() if flag]).to_dict(), **no_live_order()}
