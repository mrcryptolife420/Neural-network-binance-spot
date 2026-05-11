from .dev_quality_facade import selected_tests
def check_all_v2(changed: list[str]): return {"status": "ok", "selection": selected_tests(changed), "live_trading_enabled": False}
