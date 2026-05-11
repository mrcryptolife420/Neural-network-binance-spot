from .dev_quality_facade import safe_record
def indicator_registry(): return safe_record("indicator_registry", {"indicators": ["sma", "ema", "rsi", "macd"]})
