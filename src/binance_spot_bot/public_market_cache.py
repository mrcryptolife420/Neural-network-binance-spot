from .dev_quality_facade import data_contract
def public_market_cache_status(rows: int = 0): return data_contract("public_market_cache", rows)
