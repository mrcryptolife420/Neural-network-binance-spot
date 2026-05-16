# AI Doctor Safety Contract

AI Doctor is a local-only debug and evidence system. It never places orders, never starts live sessions, never performs recovery actions automatically and never uploads telemetry.

Debug bundles redact API keys, secrets, tokens, signatures and authorization headers. Safe env remains `LIVE_TRADING_ENABLED=false` and `KILL_SWITCH=true`.

