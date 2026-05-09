from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any


@dataclass
class DashboardSettings:
    selected_profile: str = "local-demo"
    symbol: str = "BTCUSDT"
    interval: str = "1m"
    scenario: str = "sideways"
    source: str = "auto"
    model_alias: str = ""
    risk_preset: str = "balanced"
    watchlist: list[str] = field(default_factory=lambda: ["BTCUSDT", "ETHUSDT", "BNBUSDT"])


RISK_PRESETS: dict[str, dict[str, Any]] = {
    "conservative": {
        "max_daily_loss_quote": "25",
        "max_position_quote": "10",
        "max_trades_per_day": 10,
        "min_signal_confidence": 0.35,
        "max_spread_bps": "15",
        "max_data_age_ms": 60_000,
        "default_quote_size": "5",
    },
    "balanced": {
        "max_daily_loss_quote": "50",
        "max_position_quote": "25",
        "max_trades_per_day": 25,
        "min_signal_confidence": 0.15,
        "max_spread_bps": "30",
        "max_data_age_ms": 120_000,
        "default_quote_size": "10",
    },
    "aggressive-paper-only": {
        "max_daily_loss_quote": "100",
        "max_position_quote": "50",
        "max_trades_per_day": 50,
        "min_signal_confidence": 0.05,
        "max_spread_bps": "75",
        "max_data_age_ms": 180_000,
        "default_quote_size": "15",
    },
}


class DashboardSettingsStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.dashboard_path = self.root / "dashboard.json"
        self.risk_path = self.root / "risk-presets.json"
        self.watchlist_path = self.root / "watchlists.json"

    def load(self) -> DashboardSettings:
        if not self.dashboard_path.exists():
            return DashboardSettings()
        try:
            payload = json.loads(self.dashboard_path.read_text(encoding="utf-8"))
            return DashboardSettings(**_strip_secret_keys(payload))
        except (json.JSONDecodeError, TypeError, ValueError):
            return DashboardSettings()

    def save(self, settings: DashboardSettings) -> Path:
        payload = _strip_secret_keys(asdict(settings))
        self.dashboard_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return self.dashboard_path

    def load_risk_presets(self) -> dict[str, dict[str, Any]]:
        if not self.risk_path.exists():
            self.risk_path.write_text(json.dumps(RISK_PRESETS, indent=2, sort_keys=True), encoding="utf-8")
            return dict(RISK_PRESETS)
        try:
            payload = json.loads(self.risk_path.read_text(encoding="utf-8"))
            return _strip_secret_keys(payload)
        except json.JSONDecodeError:
            return dict(RISK_PRESETS)

    def reset(self) -> DashboardSettings:
        settings = DashboardSettings()
        self.save(settings)
        return settings


def _strip_secret_keys(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {
            key: _strip_secret_keys(value)
            for key, value in payload.items()
            if key.lower() not in {"api_key", "api_secret", "binance_api_key", "binance_api_secret", "signature", "listen_key", "listenkey"}
        }
    if isinstance(payload, list):
        return [_strip_secret_keys(item) for item in payload]
    if isinstance(payload, Decimal):
        return str(payload)
    return payload
