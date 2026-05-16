from __future__ import annotations

NO_LIVE_AUTO_START_STATEMENT = "PACKAGING NEVER AUTO-STARTS LIVE TRADING"
SECRET_FREE_PACKAGE_STATEMENT = "PACKAGE ARTIFACTS MUST NOT CONTAIN RAW SECRETS"
SAFE_ENV_DEFAULTS = {"LIVE_TRADING_ENABLED": "false", "KILL_SWITCH": "true"}
FORBIDDEN_RUNTIME_ACTIONS = ("place_order", "start_live_session", "arm_live", "auto_rearm", "increase_risk_limit")

