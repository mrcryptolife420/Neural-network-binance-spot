from .safety import LiveSafetyDecision, no_live_order
def live_dry_run_account(read_only_ok: bool): return {**LiveSafetyDecision("ok" if read_only_ok else "blocked", "read_only_verify", [] if read_only_ok else ["read_only_failed"]).to_dict(), **no_live_order()}
