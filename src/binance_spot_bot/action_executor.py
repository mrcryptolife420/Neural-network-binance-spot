from .action_center import SAFE_ACTIONS
def execute_approved_action(action_type: str, approved: bool): return {"status": "executed" if approved and action_type in SAFE_ACTIONS else "blocked", "dry_run": True, "live_trading_enabled": False}
