def flaky_check_burndown(flaky: list[str]): return {"status": "ok" if not flaky else "warn", "flaky": flaky, "live_trading_enabled": False}
