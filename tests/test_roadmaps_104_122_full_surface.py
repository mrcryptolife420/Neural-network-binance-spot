from __future__ import annotations

from binance_spot_bot.dashboard_v2_facade import (
    advanced_layout,
    dashboard_v2_smoke_payload,
    extension_pack,
    market_workbench,
    parity_matrix,
    streamlit_deprecation_plan,
)
from binance_spot_bot.demo_data_validation_gate import demo_data_validation_gate
from binance_spot_bot.live_trading.automatic_disarm_rules import automatic_disarm_rules
from binance_spot_bot.live_trading.live_dry_run_account import live_dry_run_account
from binance_spot_bot.live_trading.live_execution_quality import live_execution_quality
from binance_spot_bot.live_trading.live_order_preview import live_order_preview
from binance_spot_bot.live_trading.live_session_review import live_session_review
from binance_spot_bot.live_trading.micro_position_scaling import micro_position_scaling
from binance_spot_bot.live_trading.minimal_real_order_safety import minimal_real_order_safety
from binance_spot_bot.live_trading.operator_approval_workflow import operator_approval_workflow
from binance_spot_bot.live_trading.risk_limit_calibration import risk_limit_calibration
from binance_spot_bot.live_trading.scaling_governance import scaling_governance
from binance_spot_bot.one_click_unified_launcher import one_click_unified_launcher
from binance_spot_bot.packaging_facade import production_packaging_plan, safe_update_plan
from binance_spot_bot.portfolio_experiment_orchestrator import portfolio_experiment_orchestrator
from binance_spot_bot.portfolio_rebalance_lab import portfolio_rebalance_lab
from binance_spot_bot.strategy_lab_queue import strategy_lab_queue


def test_104_dashboard_v2_realtime_contract_has_no_full_refresh():
    smoke = dashboard_v2_smoke_payload()

    assert smoke["contract"]["payload"]["full_page_refresh_required"] is False
    assert smoke["event"]["payload"]["topic"] == "runtime.snapshot"
    assert smoke["live_trading_enabled"] is False


def test_105_109_dashboard_v2_parity_deprecation_and_extension_surfaces():
    parity = parity_matrix(["overview", "demo"], ["overview", "demo"])
    deprecation = streamlit_deprecation_plan(parity_ok=True, tests_ok=True)
    layout = advanced_layout(["candles", "orders", "risk"])
    pack = extension_pack("operator", ["simple-demo", "paper-review"])

    assert parity["payload"]["parity"] is True
    assert deprecation["payload"]["eligible"] is True
    assert layout["payload"]["multi_panel"] is True
    assert pack["payload"]["pluginless"] is True


def test_112_115_market_strategy_portfolio_research_is_paper_only():
    market = market_workbench(["btcusdt", "ethusdt"])
    queue = strategy_lab_queue(["mean-reversion"])
    orchestrator = portfolio_experiment_orchestrator(["BTCUSDT", "ETHUSDT"])
    rebalance = portfolio_rebalance_lab({"BTCUSDT": 0.5, "ETHUSDT": 0.5})

    assert market["payload"]["paper_analytics_only"] is True
    assert queue["payload"]["paper_only"] is True
    assert orchestrator["payload"]["simulation_only"] is True
    assert rebalance["payload"]["walk_forward"] is True


def test_116_117_one_click_and_demo_data_gate_remain_safe():
    launcher = one_click_unified_launcher("demo")
    gate = demo_data_validation_gate(100, quality_ok=True)
    blocked = demo_data_validation_gate(0, quality_ok=True)

    assert launcher["payload"]["opens_dashboard"] is True
    assert launcher["payload"]["safe_live_gate"] is True
    assert gate["status"] == "ok"
    assert blocked["status"] == "blocked"


def test_118_live_dry_run_and_order_preview_never_submit_order():
    account = live_dry_run_account(read_only_ok=True)
    preview = live_order_preview({"symbol": "BTCUSDT", "quote": "5"})
    armed = minimal_real_order_safety("")

    assert account["live_order_submitted"] is False
    assert preview["signed_order_endpoint_called"] is False
    assert preview["preview_hash"]
    assert armed["status"] == "blocked"


def test_119_controlled_live_session_scaling_requires_approval_and_disarms():
    blocked = micro_position_scaling(1, 3, approved=True)
    approved = micro_position_scaling(1, 2, approved=True)
    disarm = automatic_disarm_rules(["heartbeat_failed"])

    assert blocked["status"] == "blocked"
    assert approved["status"] == "approved"
    assert disarm["status"] == "disarm"
    assert disarm["live_order_submitted"] is False


def test_120_review_scaling_risk_calibration_approval_workflow():
    review = live_session_review(evidence_present=False)
    quality = live_execution_quality(25)
    calibration = risk_limit_calibration(current=10, proposed=20)
    scaling = scaling_governance(1, 2, "A", approved=False)
    approval = operator_approval_workflow("APPROVE_LIVE_SCALING_REVIEW")

    assert review["status"] == "blocked"
    assert quality["status"] == "warn"
    assert calibration["status"] == "approval_required"
    assert scaling["decision"] == "blocked"
    assert approval["status"] == "approved"


def test_122_packaging_safe_update_rollback_plan():
    packaging = production_packaging_plan()
    update = safe_update_plan("1.0.0")

    assert packaging["payload"]["desktop_shortcut"] is True
    assert packaging["payload"]["offline_recovery"] is True
    assert update["payload"]["requires_backup"] is True
    assert update["live_trading_enabled"] is False
