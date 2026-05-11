from .dev_quality_facade import runtime_event
def runtime_market_service(symbol: str): return runtime_event("market_service", {"symbol": symbol})
