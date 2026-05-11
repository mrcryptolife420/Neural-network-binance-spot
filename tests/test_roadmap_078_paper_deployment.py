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
from binance_spot_bot.paper_deployment import (
    PaperDeploymentStore,
    create_paper_deployment_plan,
    evaluate_paper_deployment,
    rollback_plan,
    run_paper_deployment_cycle,
    write_daily_strategy_report,
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


def test_paper_deployment_plan_version_lock_store_and_report() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        s = settings(tmp)
        plan = create_paper_deployment_plan(s, "adaptive", "candidate-a", ["btcusdt"], calibration_gate={"status": "paper_approved"})
        store = PaperDeploymentStore(s.data_dir / "paper-deployments")
        plan_path = store.save_plan(plan)
        loaded = store.load_plan(plan.deployment_id)
        evaluation = evaluate_paper_deployment(plan, [{"pnl": "2.5", "confidence": 0.57}])
        eval_path = store.save_evaluation(evaluation)
        reports = write_daily_strategy_report(s, plan, evaluation)
        assert Path(plan_path).exists()
        assert Path(eval_path).exists()
        assert Path(reports["markdown"]).exists()

    assert plan.status == "planned"
    assert plan.version_lock == "adaptive:candidate-a:balanced"
    assert loaded.deployment_id == plan.deployment_id
    assert evaluation.watchdog_status == "clear"


def test_paper_deployment_watchdog_triggers_auto_rollback() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        plan = create_paper_deployment_plan(settings(tmp), "adaptive", "candidate-a", ["BTCUSDT"])
        evaluation = evaluate_paper_deployment(
            plan,
            [{"pnl": "-30", "confidence": 0.95}, {"pnl": "-10", "confidence": 0.98}],
            max_drawdown=Decimal("5"),
        )
        rollback = rollback_plan(plan, evaluation)

    assert evaluation.rollback_required is True
    assert "drawdown_limit_breached" in evaluation.reasons
    assert rollback["target_preset"] == "conservative"
    assert rollback["safe_mode"] == "paper_only"


def test_paper_deployment_cycle_and_cli_are_paper_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        s = settings(tmp)
        payload = run_paper_deployment_cycle(s, "adaptive", "candidate-a", ["BTCUSDT"], [{"pnl": "1", "confidence": 0.55}])
        env = {"DATA_DIR": str(Path(tmp) / "cli-data"), "AUDIT_LOG_PATH": str(Path(tmp) / "cli-data" / "audit" / "events.jsonl")}
        buf = io.StringIO()
        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["spot-bot", "paper-deployment-cycle", "--json"]), redirect_stdout(buf):
            cli_main()
        cli_payload = json.loads(buf.getvalue())

    assert payload["plan"]["live_trading_enabled"] is False
    assert payload["evaluation"]["status"] == "healthy"
    assert cli_payload["rollback"]["safe_mode"] == "paper_only"
