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
from binance_spot_bot.paper_portfolio_ops import PaperStrategy, build_portfolio_allocation
from binance_spot_bot.portfolio_optimization import optimize_portfolio_policy, search_risk_budgets, select_robust_policy
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


def plan():
    return build_portfolio_allocation(
        [PaperStrategy("trend", 0.8, ["BTCUSDT"]), PaperStrategy("mean", 0.65, ["ETHUSDT"])],
        Decimal("1000"),
    )


def test_risk_budget_search_selects_conservative_robust_policy() -> None:
    search = search_risk_budgets(plan())
    card = select_robust_policy(plan(), search)

    assert len(search) == 3
    assert card.status == "paper_selected"
    assert card.live_trading_enabled is False
    assert card.selection_reason == "stress_pass_then_highest_robustness_with_conservative_tiebreak"


def test_optimize_portfolio_policy_writes_policy_card() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        payload = optimize_portfolio_policy(settings(tmp), plan())
        assert Path(payload["paths"]["latest"]).exists()

    assert payload["policy"]["status"] == "paper_selected"
    assert payload["policy"]["live_trading_enabled"] is False


def test_portfolio_optimization_cli_exports_json() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        env = {"DATA_DIR": str(Path(tmp) / "data"), "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl")}
        buf = io.StringIO()
        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "paper-portfolio-optimize", "--json"]), redirect_stdout(buf):
            cli_main()
        payload = json.loads(buf.getvalue())

    assert payload["policy"]["status"] == "paper_selected"
    assert payload["paths"]["latest"].endswith("latest-policy-card.json")
