from .action_center import SAFE_ACTIONS
def validate_action(action_type: str): return {"status": "ok" if action_type in SAFE_ACTIONS else "blocked", "live_trading_enabled": False}
