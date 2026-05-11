from .allocation_policy import allocation_policy
def portfolio_allocation_engine(weights: dict[str, float]): return allocation_policy(weights)
