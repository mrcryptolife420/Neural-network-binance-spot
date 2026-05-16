# Packaging Safety Contract

Packaging, installer, update, rollback and recovery tooling never starts live trading, never arms live profiles and never places orders.

Safe defaults:

* `LIVE_TRADING_ENABLED=false`
* `KILL_SWITCH=true`
* raw secrets are excluded from package, backup, recovery kit and evidence artifacts

