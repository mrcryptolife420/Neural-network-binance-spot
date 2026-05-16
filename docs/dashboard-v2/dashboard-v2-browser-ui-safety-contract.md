# Dashboard V2 Browser UI Safety Contract

Dashboard V2 is a localhost-only browser UI. It never places live orders, never arms live sessions, never stores API keys in browser storage, and never loads external scripts, fonts or telemetry.

Required visible safety state:

* `LIVE_TRADING_ENABLED=false`
* `KILL_SWITCH=true`
* live pages are locked by default
* Streamlit is legacy fallback only

