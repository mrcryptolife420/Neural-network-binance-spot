from __future__ import annotations

import io
import json
import os
import tempfile
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.cli import main as cli_main
from binance_spot_bot.config import BotSettings
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.paper_portfolio_ops import (
    PaperStrategy,
    build_portfolio_allocation,
    portfolio_attribution,
    portfolio_watchdog,
    rotate_strategies,
    run_portfolio_operations,
)
from binance_spot_bot.portfolio import Portfolio
from binance_spot_bot.types import TradingMode


def settings(tmp: str) -> BotSettings:
    return BotSettings(
        app_env="local",
        trading_mode=TradingMode.TESTNET,
        binance_base_url="https://api.binance.com",
        binance_testnet_base_url="https://demo-api.binance.com",
        binance_api_key="",
        binance_api_secret="",
        live_trading_enabled=False,
        kill_switch=False,
        manual_live_approval="",
        max_daily_loss_quote=Decimal("50"),
        max_position_quote=Decimal("25"),
        max_trades_per_day=5,
        min_signal_confidence=0.1,
        max_spread_bps=Decimal("50"),
        data_dir=Path(tmp) / "data",
        audit_log_path=Path(tmp) / "data" / "audit" / "events.jsonl",
        exchange_profile=BINANCE_DEMO_SPOT_PROFILE,
        binance_demo_base_url="https://demo-api.binance.com",
    )


def strategies() -> list[PaperStrategy]:
    return [
        PaperStrategy("trend", 0.80, ["BTCUSDT", "ETHUSDT"]),
        PaperStrategy("mean", 0.65, ["ETHUSDT", "BNBUSDT"]),
        PaperStrategy("weak", 0.20, ["ADAUSDT"], status="watch"),
    ]


def test_portfolio_allocation_conflicts_and_rotation_policy() -> None:
    plan = build_portfolio_allocation(strategies(), Decimal("1000"))
    attribution = portfolio_attribution([{"strategy_id": "trend", "pnl": "5"}, {"strategy_id": "mean", "pnl": "-6"}])
    rotation = rotate_strategies(plan, attribution)

    assert plan.live_trading_enabled is False
    assert plan.total_quote_budget == Decimal("1000")
    assert any(conflict["symbol"] == "ETHUSDT" for conflict in plan.conflicts)
    assert any(row["action"] == "pause" for row in rotation)


def test_portfolio_watchdog_and_evidence() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        s = settings(tmp)
        payload = run_portfolio_operations(
            s,
            strategies(),
            Decimal("1000"),
            [{"strategy_id": "trend", "pnl": "2"}, {"strategy_id": "mean", "pnl": "1"}],
        )
        assert Path(payload["evidence"]["latest"]).exists()

    assert payload["watchdog"]["status"] == "healthy"
    assert payload["plan"]["risk_limits"]["max_strategy_weight"] == "0.40"
    assert payload["plan"]["live_trading_enabled"] is False


def test_portfolio_watchdog_blocks_exposure_and_cli_runs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        plan = build_portfolio_allocation([PaperStrategy("trend", 1.0, ["BTCUSDT"])], Decimal("10"))
        portfolio = Portfolio()
        portfolio.set_balance("USDT", Decimal("100"))
        portfolio.buy("BTCUSDT", "USDT", Decimal("100"), Decimal("100"), fee_bps=Decimal("0"))
        watchdog = portfolio_watchdog(plan, portfolio, {"BTCUSDT": Decimal("100")})
        env = {"DATA_DIR": str(Path(tmp) / "data"), "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl")}
        buf = io.StringIO()
        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "paper-portfolio-ops", "--json"]), redirect_stdout(buf):
            cli_main()
        cli_payload = json.loads(buf.getvalue())

    assert watchdog["status"] == "blocked"
    assert "portfolio_exposure_limit" in watchdog["blockers"]
    assert cli_payload["plan"]["live_trading_enabled"] is False
