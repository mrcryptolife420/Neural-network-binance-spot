def paper_portfolio_rebalance(drift: float): return {"status": "rebalance" if drift > 0.1 else "hold", "live_trading_enabled": False}
