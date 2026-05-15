from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


@dataclass(frozen=True)
class DashboardV2OperatorPreferences:
    default_workspace: str = "operator_overview"
    default_mode: str = "demo"
    default_source: str = "demo"
    default_symbol: str = "BTCUSDT"
    default_interval: str = "1m"
    chart_point_limit: int = 500
    theme: str = "system"
    compact_mode: bool = False
    advanced_panels_visible: bool = True
    notifications_enabled: bool = True
    local_metrics_retention_days: int = 30
    disable_local_ux_metrics: bool = False
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_dashboard_payload(asdict(self))


def validate_operator_preferences(prefs: DashboardV2OperatorPreferences) -> dict[str, Any]:
    blockers: list[str] = []
    if prefs.default_mode == "live":
        blockers.append("live mode blocked")
    if prefs.theme not in {"system", "light", "dark"}:
        blockers.append("invalid theme")
    if prefs.chart_point_limit < 50 or prefs.chart_point_limit > 5000:
        blockers.append("chart point limit outside safe bounds")
    if prefs.live_trading_enabled:
        blockers.append("live_trading_enabled must be false")
    return {"status": "ok" if not blockers else "blocked", "blockers": blockers, "live_trading_enabled": False}


def load_operator_preferences(path: Path) -> DashboardV2OperatorPreferences:
    if not path.exists():
        return DashboardV2OperatorPreferences()
    return DashboardV2OperatorPreferences(**redact_dashboard_payload(json.loads(path.read_text(encoding="utf-8"))))


def save_operator_preferences(path: Path, prefs: DashboardV2OperatorPreferences) -> dict[str, Any]:
    result = validate_operator_preferences(prefs)
    if result["status"] != "ok":
        return result
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(prefs.to_dict(), indent=2), encoding="utf-8")
    return {"status": "ok", "path": str(path), "preferences": prefs.to_dict(), "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def operator_preferences_payload(root: Path | str = ".") -> dict[str, Any]:
    path = Path(root) / "data" / "dashboard-v2" / "preferences.json"
    prefs = load_operator_preferences(path)
    return {"status": "ok", "path": str(path), "preferences": prefs.to_dict(), "validation": validate_operator_preferences(prefs), "live_trading_enabled": False}
