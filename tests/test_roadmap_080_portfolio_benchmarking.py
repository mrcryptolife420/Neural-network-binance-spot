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
from binance_spot_bot.portfolio_benchmarking import (
    StressScenario,
    benchmark_allocations,
    correlation_stress,
    replay_portfolio_scenario,
    validate_rotation_robustness,
    write_benchmark_report,
)
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
        [PaperStrategy("trend", 0.80, ["BTCUSDT"]), PaperStrategy("mean", 0.65, ["ETHUSDT"])],
        Decimal("1000"),
    )


def test_scenario_replay_benchmark_and_report_are_reproducible() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        p = plan()
        replay = replay_portfolio_scenario(p, StressScenario("bear", price_shock_bps=-200, spread_shock_bps=50))
        benchmark_a = benchmark_allocations(p)
        benchmark_b = benchmark_allocations(p)
        reports = write_benchmark_report(settings(tmp), benchmark_a)
        assert Path(reports["latest"]).exists()

    assert replay["total_stressed_loss"] != "0"
    assert benchmark_a["reproducibility_hash"] == benchmark_b["reproducibility_hash"]
    assert benchmark_a["live_trading_enabled"] is False


def test_correlation_and_rotation_robustness() -> None:
    corr = correlation_stress({"BTCUSDT": [0.1, 0.2, 0.3], "ETHUSDT": [0.1, 0.2, 0.31], "BNBUSDT": [0.3, 0.2, 0.1]})
    rotation = validate_rotation_robustness([{"action": "eligible"}, {"action": "pause"}, {"action": "eligible"}])

    assert corr["status"] == "review"
    assert any(row["status"] == "crowded" for row in corr["pairs"])
    assert rotation["status"] == "pass"


def test_portfolio_benchmark_cli_exports_json() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        env = {"DATA_DIR": str(Path(tmp) / "data"), "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl")}
        buf = io.StringIO()
        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "paper-portfolio-benchmark", "--json"]), redirect_stdout(buf):
            cli_main()
        payload = json.loads(buf.getvalue())

    assert payload["status"] in {"pass", "review"}
    assert payload["reports"]["latest"].endswith("latest.json")
