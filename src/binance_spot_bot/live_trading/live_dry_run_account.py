from .live_account_verifier import FakeLiveReadOnlyAdapter, verify_live_read_only_account
from .safety import LiveSafetyDecision, no_live_order


def live_dry_run_account(read_only_ok: bool):
    verified = verify_live_read_only_account(FakeLiveReadOnlyAdapter(account_ok=read_only_ok))
    return {**LiveSafetyDecision("ok" if read_only_ok else "blocked", "read_only_verify", [] if read_only_ok else ["read_only_failed"]).to_dict(), **verified, **no_live_order()}
