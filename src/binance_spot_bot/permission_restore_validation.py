from .permission_profiles import permission_matrix
def permission_restore_validation(): return {"status": "ok", "matrix": permission_matrix(), "live_trading_enabled": False}
