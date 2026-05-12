# Intelligent Test Selection Safety Contract

- Test selection is local-only and explainable.
- Commands must use `LIVE_TRADING_ENABLED=false` and `KILL_SWITCH=true`.
- Critical safety changes cannot be approved by fast profile only.
- Security/redaction changes require security and redaction checks.
- Dashboard changes require dashboard smoke and browser smoke when relevant.
- Live trading enabled: false.
