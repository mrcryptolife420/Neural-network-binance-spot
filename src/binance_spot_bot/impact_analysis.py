from .dev_quality_facade import regression_risk, selected_tests
def impact_analysis(changed: list[str]): return {"risk": regression_risk(changed), "tests": selected_tests(changed), "live_trading_enabled": False}
