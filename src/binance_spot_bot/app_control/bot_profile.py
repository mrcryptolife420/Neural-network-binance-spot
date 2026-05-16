from __future__ import annotations

import re
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any

from . import NO_LIVE_AUTO_START_STATEMENT
from binance_spot_bot.portfolio_lab.common import json_write, redact_value, status_from_blockers


class BotProfileMode(str, Enum):
    BACKTEST = "backtest"
    PAPER = "paper"
    DEMO_SPOT = "demo_spot"
    TESTNET = "testnet"
    LIVE_LOCKED = "live_locked"
    LIVE_ARMED = "live_armed"
    DISABLED = "disabled"


@dataclass(frozen=True)
class BotProfileSecretsRef:
    ref_type: str = "env"
    key_ref: str = "BINANCE_API_KEY"
    secret_ref: str = "BINANCE_API_SECRET"
    fingerprint: str = ""


@dataclass(frozen=True)
class BotProfileTrainingGate:
    requires_demo_training_evidence: bool = False
    required_demo_sessions: int = 0
    required_min_demo_fills: int = 0
    required_dataset_quality_score: float = 0.0
    required_validation_grade: str = ""


@dataclass(frozen=True)
class BotProfileRisk:
    max_daily_loss_quote: float = 25.0
    max_position_quote: float = 100.0
    max_trades_per_day: int = 10
    min_signal_confidence: float = 0.55
    max_spread_bps: float = 25.0
    starting_quote_balance: float = 1000.0
    risk_preset: str = "conservative"


@dataclass(frozen=True)
class BotProfileModel:
    model_alias: str = "tiny_nn_v1"
    strategy_id: str = "rule_baseline"


@dataclass(frozen=True)
class BotProfile:
    profile_id: str
    name: str
    description: str
    mode: str
    exchange_profile: str = "binance"
    base_url: str = "https://api.binance.com/api"
    symbol: str = "BTCUSDT"
    watchlist_id: str = "majors"
    interval: str = "1m"
    data_source: str = "fixture"
    model: BotProfileModel = field(default_factory=BotProfileModel)
    risk: BotProfileRisk = field(default_factory=BotProfileRisk)
    secret_ref: BotProfileSecretsRef = field(default_factory=BotProfileSecretsRef)
    training_gate: BotProfileTrainingGate = field(default_factory=BotProfileTrainingGate)
    dashboard_workspace_id: str = "overview"
    auto_open_dashboard: bool = True
    auto_fetch_data: bool = True
    auto_start_runtime: bool = False
    live_trading_enabled: bool = False
    kill_switch: bool = True
    manual_live_approval: str = ""
    no_live_auto_start_statement: str = NO_LIVE_AUTO_START_STATEMENT
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    updated_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))


@dataclass(frozen=True)
class BotProfileValidationResult:
    status: str
    blockers: list[str]
    warnings: list[str]
    live_trading_enabled: bool = False


SECRET_PATTERNS = (re.compile(r"[A-Za-z0-9]{48,}"), re.compile(r"(?i)(api[_-]?key|secret)\s*[:=]\s*[A-Za-z0-9]{12,}"))
SAFE_BASE_URLS = {
    "https://api.binance.com/api",
    "https://testnet.binance.vision/api",
    "https://demo-api.binance.com/api",
    "fixture://local",
}


def bot_profile_to_dict(profile: BotProfile) -> dict[str, Any]:
    return redact_value(asdict(profile))


def validate_bot_profile(profile: BotProfile) -> BotProfileValidationResult:
    blockers: list[str] = []
    warnings: list[str] = []
    payload = str(asdict(profile))
    if any(pattern.search(payload) for pattern in SECRET_PATTERNS):
        blockers.append("secret-like value in profile")
    if profile.exchange_profile not in {"binance", "binance_demo", "binance_testnet", "local"}:
        blockers.append("unknown exchange profile")
    if profile.base_url not in SAFE_BASE_URLS:
        blockers.append("unsafe base_url")
    if not re.match(r"^[A-Z0-9]{5,20}$", profile.symbol):
        blockers.append("invalid symbol")
    if profile.interval not in {"1m", "3m", "5m", "15m", "1h", "1d"}:
        blockers.append("invalid interval")
    if not profile.risk.risk_preset:
        blockers.append("missing risk preset")
    if re.search(r"\b(buy|sell|guaranteed profit)\b", payload, re.IGNORECASE):
        blockers.append("unsafe advice/profit wording")
    live_mode = profile.mode in {BotProfileMode.LIVE_LOCKED.value, BotProfileMode.LIVE_ARMED.value}
    if live_mode:
        if profile.auto_start_runtime:
            blockers.append("live mode cannot auto_start_runtime")
        if not profile.training_gate.requires_demo_training_evidence:
            blockers.append("live mode requires demo training evidence")
        if profile.training_gate.required_demo_sessions <= 0:
            blockers.append("live mode requires demo sessions")
        if profile.training_gate.required_min_demo_fills <= 0:
            blockers.append("live mode requires demo fills")
        if profile.training_gate.required_dataset_quality_score <= 0:
            blockers.append("live mode requires dataset quality threshold")
        if not profile.training_gate.required_validation_grade:
            blockers.append("live mode requires validation grade")
        if profile.risk.max_daily_loss_quote <= 0 or profile.risk.max_position_quote <= 0 or profile.risk.max_trades_per_day <= 0:
            blockers.append("live mode requires risk limits")
        if not profile.kill_switch:
            blockers.append("live mode requires kill switch before arming")
        if profile.live_trading_enabled and profile.manual_live_approval != "approved_after_gates":
            blockers.append("live trading flag requires manual approval after gates")
    return BotProfileValidationResult(status_from_blockers(blockers, warnings), blockers, warnings)


def built_in_profiles() -> list[BotProfile]:
    live_gate = BotProfileTrainingGate(True, 3, 10, 85.0, "B")
    return [
        BotProfile("backtest-local-btcusdt", "Backtest Local BTCUSDT", "Local fixture backtest profile", BotProfileMode.BACKTEST.value, base_url="fixture://local", auto_start_runtime=True),
        BotProfile("paper-btcusdt-safe", "Paper BTCUSDT Safe", "Local paper profile", BotProfileMode.PAPER.value, base_url="fixture://local", auto_start_runtime=True),
        BotProfile("binance-demo-spot-safe", "Binance Demo Spot Safe", "Demo spot profile with guarded start", BotProfileMode.DEMO_SPOT.value, exchange_profile="binance_demo", base_url="https://demo-api.binance.com/api"),
        BotProfile("binance-spot-testnet-safe", "Binance Spot Testnet Safe", "Spot testnet profile with guarded start", BotProfileMode.TESTNET.value, exchange_profile="binance_testnet", base_url="https://testnet.binance.vision/api"),
        BotProfile("live-locked-training-required-template", "Live Locked Training Required", "Live profile locked behind demo training evidence", BotProfileMode.LIVE_LOCKED.value, training_gate=live_gate),
    ]


def write_bot_profile_report(root: Path, profile: BotProfile) -> dict[str, Any]:
    validation = validate_bot_profile(profile)
    payload = {"status": validation.status, "profile": bot_profile_to_dict(profile), "validation": asdict(validation), "live_trading_enabled": False}
    return json_write(root / "data" / "app-control" / "profiles" / "reports" / f"{profile.profile_id}.json", payload)

