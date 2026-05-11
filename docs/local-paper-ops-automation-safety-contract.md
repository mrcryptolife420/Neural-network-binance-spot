# Local Paper Ops Automation Safety Contract

Local ops automation may only execute allowlisted local paper/read-only commands. It must not run live mode, signed order endpoints, account endpoints, external uploads, shell-expanded commands, or commands carrying secrets.

Required environment for executed jobs:

- `LIVE_TRADING_ENABLED=false`
- `KILL_SWITCH=true`

Dangerous actions require explicit operator confirmation and are not eligible for unattended scheduling.
