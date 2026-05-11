from .local_paper_os_facade import safe_record
def portfolio_rebalance_lab(weights: dict[str, float]): return safe_record("portfolio_rebalance_lab", {"weights": weights, "walk_forward": True})
