def live_session_scorecard(blockers: list[str]): return {"grade": "F" if blockers else "A", "blockers": blockers, "live_order_submitted": False, "live_trading_enabled": False}
