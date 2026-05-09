from __future__ import annotations

import os
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .exchange_profiles import BINANCE_DEMO_SPOT_PROFILE, LOCAL_DEMO_PROFILE, profile_for
from .types import TradingMode


class ConfigError(ValueError):
    pass


def _bool_env(value: str | None, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _decimal_env(name: str, default: str) -> Decimal:
    raw = os.getenv(name, default)
    try:
        return Decimal(raw)
    except InvalidOperation as exc:
        raise ConfigError(f"{name} must be a decimal value") from exc


@dataclass(frozen=True)
class BotSettings:
    app_env: str
    trading_mode: TradingMode
    binance_base_url: str
    binance_testnet_base_url: str
    binance_api_key: str
    binance_api_secret: str
    live_trading_enabled: bool
    kill_switch: bool
    manual_live_approval: str
    max_daily_loss_quote: Decimal
    max_position_quote: Decimal
    max_trades_per_day: int
    min_signal_confidence: float
    max_spread_bps: Decimal
    data_dir: Path
    audit_log_path: Path
    exchange_profile: str = LOCAL_DEMO_PROFILE
    binance_demo_base_url: str = "https://demo-api.binance.com"

    @classmethod
    def from_env(cls) -> "BotSettings":
        mode = TradingMode(os.getenv("TRADING_MODE", "disabled").strip().lower())
        exchange_profile = os.getenv("EXCHANGE_PROFILE", LOCAL_DEMO_PROFILE).strip()
        api_base_alias = os.getenv("BINANCE_API_BASE_URL", "").rstrip("/")
        demo_base = os.getenv("BINANCE_DEMO_BASE_URL", api_base_alias or "https://demo-api.binance.com").rstrip("/")
        testnet_default = (
            demo_base
            if exchange_profile == BINANCE_DEMO_SPOT_PROFILE and api_base_alias
            else "https://testnet.binance.vision"
        )
        return cls(
            app_env=os.getenv("APP_ENV", "local"),
            trading_mode=mode,
            binance_base_url=os.getenv("BINANCE_BASE_URL", "https://api.binance.com").rstrip("/"),
            binance_testnet_base_url=os.getenv(
                "BINANCE_TESTNET_BASE_URL", api_base_alias or testnet_default
            ).rstrip("/"),
            binance_api_key=os.getenv("BINANCE_API_KEY", ""),
            binance_api_secret=os.getenv("BINANCE_API_SECRET", ""),
            live_trading_enabled=_bool_env(os.getenv("LIVE_TRADING_ENABLED"), False),
            kill_switch=_bool_env(os.getenv("KILL_SWITCH"), True),
            manual_live_approval=os.getenv("MANUAL_LIVE_APPROVAL", ""),
            max_daily_loss_quote=_decimal_env("MAX_DAILY_LOSS_QUOTE", "0"),
            max_position_quote=_decimal_env("MAX_POSITION_QUOTE", "0"),
            max_trades_per_day=int(os.getenv("MAX_TRADES_PER_DAY", "0")),
            min_signal_confidence=float(os.getenv("MIN_SIGNAL_CONFIDENCE", "0.65")),
            max_spread_bps=_decimal_env("MAX_SPREAD_BPS", "20"),
            data_dir=Path(os.getenv("DATA_DIR", "data")),
            audit_log_path=Path(os.getenv("AUDIT_LOG_PATH", "data/audit/events.jsonl")),
            exchange_profile=exchange_profile,
            binance_demo_base_url=demo_base,
        )

    @property
    def active_base_url(self) -> str:
        if self.exchange_profile == BINANCE_DEMO_SPOT_PROFILE:
            return self.binance_demo_base_url
        if self.trading_mode == TradingMode.TESTNET:
            return self.binance_testnet_base_url
        return self.binance_base_url

    @property
    def active_profile(self):
        return profile_for(self.exchange_profile)

    def validate_startup(self) -> None:
        if self.trading_mode in {TradingMode.TESTNET, TradingMode.LIVE}:
            if not self.binance_api_key or not self.binance_api_secret:
                raise ConfigError("Signed trading modes require BINANCE_API_KEY and BINANCE_API_SECRET")

        if self.trading_mode == TradingMode.LIVE:
            self.validate_live_readiness()

    def validate_live_readiness(self) -> None:
        failures: list[str] = []
        if self.app_env != "live":
            failures.append("APP_ENV must be live")
        if not self.live_trading_enabled:
            failures.append("LIVE_TRADING_ENABLED must be true")
        if self.kill_switch:
            failures.append("KILL_SWITCH must be false")
        if self.manual_live_approval != "I_UNDERSTAND_LIVE_SPOT_TRADING_RISK":
            failures.append("MANUAL_LIVE_APPROVAL is missing the required approval phrase")
        if self.max_daily_loss_quote <= 0:
            failures.append("MAX_DAILY_LOSS_QUOTE must be greater than 0")
        if self.max_position_quote <= 0:
            failures.append("MAX_POSITION_QUOTE must be greater than 0")
        if self.max_trades_per_day <= 0:
            failures.append("MAX_TRADES_PER_DAY must be greater than 0")
        if not self.binance_api_key or not self.binance_api_secret:
            failures.append("Binance API credentials are required")
        if failures:
            raise ConfigError("Live trading blocked: " + "; ".join(failures))
