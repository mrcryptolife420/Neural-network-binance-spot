from __future__ import annotations

import tempfile
from decimal import Decimal
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.exchange_profiles import BINANCE_DEMO_SPOT_PROFILE
from binance_spot_bot.paper_os import (
    RuntimeEventBus,
    action_center_proposal,
    build_public_data_warmup_plan,
    calibrate_strategy_confidence,
    champion_challenger_governance,
    dashboard_payload_budget,
    disaster_recovery_plan,
    ensemble_vote,
    feature_contract_report,
    indicator_readiness,
    local_ops_job_plan,
    metrics_warehouse_snapshot,
    model_experiment_card,
    operator_manual_payload,
    optimize_risk_budget,
    paper_deployment_control,
    paper_os_audit,
    performance_budget_report,
    permission_profile,
    portfolio_allocation_policy,
    prioritize_roadmaps,
    release_upgrade_plan,
    repository_knowledge_graph,
    roadmap_execution_status,
    safe_ops_assistant_answer,
    select_tests_for_changes,
    shadow_drift_report,
    stabilization_backlog,
    stress_test_policy,
    write_paper_os_evidence,
)
from binance_spot_bot.types import Candle, TradingMode


def _settings(tmp: str) -> BotSettings:
    return BotSettings(
        app_env="local",
        trading_mode=TradingMode.TESTNET,
        binance_base_url="https://api.binance.com",
        binance_testnet_base_url="https://demo-api.binance.com",
        binance_api_key="demo-key",
        binance_api_secret="demo-secret",
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


def _candles(count: int = 80, start: Decimal = Decimal("100")) -> list[Candle]:
    rows = []
    for index in range(count):
        close = start + Decimal(index) * Decimal("0.25")
        rows.append(
            Candle(
                open_time_ms=1_700_000_000_000 + index * 60_000,
                open=close - Decimal("0.1"),
                high=close + Decimal("0.5"),
                low=close - Decimal("0.5"),
                close=close,
                volume=Decimal("10"),
                close_time_ms=1_700_000_059_999 + index * 60_000,
                quote_volume=Decimal("1000"),
                trade_count=20,
            )
        )
    return rows


def test_roadmap_prioritization_and_public_data_warmup_are_dependency_ordered() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        roadmap_dir = Path(tmp) / "Roadmap docs"
        roadmap_dir.mkdir()
        for number in [100, 76, 83, 97]:
            (roadmap_dir / f"{number:03d}-roadmap.md").write_text("# roadmap", encoding="utf-8")
        priorities = prioritize_roadmaps(roadmap_dir)
        plan = build_public_data_warmup_plan(["btcusdt", "ETHUSDT", "BTCUSDT"], min_candles=160)

    assert [item["number"] for item in priorities] == [76, 83, 97, 100]
    assert plan["status"] == "ready"
    assert len(plan["rows"]) == 8
    assert all(row["read_only"] for row in plan["rows"])


def test_indicator_strategy_deployment_and_portfolio_chain_stays_paper_only() -> None:
    candles = {"BTCUSDT": _candles(), "ETHUSDT": _candles(start=Decimal("50"))}
    readiness = indicator_readiness(candles)
    calibration = calibrate_strategy_confidence(candles)
    deployment = paper_deployment_control("adaptive-indicator", calibration)
    allocation = portfolio_allocation_policy({"BTCUSDT": 0.8, "ETHUSDT": 0.6}, Decimal("1000"))
    stress = stress_test_policy(allocation)
    optimized = optimize_risk_budget(allocation, stress)
    governance = champion_challenger_governance("balanced", {"balanced": 0.62, "trend": 0.71})

    assert readiness["status"] == "ready"
    assert calibration["promotion_gate"] == "paper_only"
    assert deployment["mode"] == "paper"
    assert deployment["no_live_contract"]["live_trading"] == "disabled"
    assert allocation["status"] == "ready"
    assert stress["replay_reproducible"] is True
    assert optimized["selection"] == "conservative_robust_allocation"
    assert governance["ab_experiment_mode"] == "paper_only"


def test_local_ops_security_recovery_release_and_safe_assistant_contracts() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        settings = _settings(tmp)
        settings.data_dir.mkdir(parents=True)
        (settings.data_dir / "artifact.json").write_text("{}", encoding="utf-8")
        recovery = disaster_recovery_plan(settings)

    jobs = local_ops_job_plan()
    metrics = metrics_warehouse_snapshot([{"pnl": 1.5, "latency_ms": 100}, {"pnl": -0.5, "latency_ms": 2500}])
    answer = safe_ops_assistant_answer("mag ik live traden?", {"status": "ok"})
    proposal = action_center_proposal("export report")
    profile = permission_profile("operator")
    release = release_upgrade_plan("0.1.0", "0.2.0")

    assert jobs["status"] == "ready"
    assert metrics["anomaly"] is True
    assert answer["allowed"] is False
    assert proposal["status"] == "pending_approval"
    assert profile["live_trading_permission"] is False
    assert recovery["restore_preview"] is True
    assert release["downgrade_safe"] is True


def test_developer_runtime_model_monitoring_and_operator_os_audit() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "src" / "binance_spot_bot").mkdir(parents=True)
        (root / "src" / "binance_spot_bot" / "runtime.py").write_text("", encoding="utf-8")
        (root / "tests").mkdir()
        (root / "tests" / "test_demo.py").write_text("", encoding="utf-8")
        roadmap_dir = root / "Roadmap docs"
        roadmap_dir.mkdir()
        (roadmap_dir / "076-roadmap.md").write_text("# roadmap", encoding="utf-8")
        settings = _settings(tmp)
        settings.data_dir.mkdir(parents=True)

        roadmap_status = roadmap_execution_status(roadmap_dir)
        graph = repository_knowledge_graph(root)
        audit = paper_os_audit(root, settings, roadmap_dir)
        evidence_path = write_paper_os_evidence(settings, audit)
        assert evidence_path.exists()

    selected = select_tests_for_changes(["src/binance_spot_bot/runtime.py", "src/binance_spot_bot/ui/streamlit_app.py"])
    perf = performance_budget_report([{"duration_ms": 100}, {"duration_ms": 1400}])
    payload = dashboard_payload_budget({"candles": list(range(20)), "audit": list(range(250))})
    bus = RuntimeEventBus(max_events=2)
    bus.publish("snapshot", "btcusdt", {"candles": [1, 2, 3], "status": "running"})
    drained = bus.drain("snapshot")
    contract = feature_contract_report([{"values": {"rsi": 55, "ema": 100}}], {"rsi", "ema"})
    card = model_experiment_card("candidate-a", {"walkforward_score": 0.61}, contract)
    drift = shadow_drift_report([0.1, 0.2, 0.3], [0.11, 0.21, 0.31])
    vote = ensemble_vote([{"signal": "BUY", "confidence": 0.7, "weight": 1.0}, {"signal": "HOLD", "confidence": 0.4}])
    backlog = stabilization_backlog(audit)
    manual = operator_manual_payload()

    assert roadmap_status["open_roadmaps"] == 1
    assert graph["nodes"]["src"] == 1
    assert audit["status"] == "pass"
    assert selected["profile"] == "standard"
    assert perf["status"] == "pass"
    assert payload["status"] == "review"
    assert drained[0]["payload"]["candles"]["count"] == 3
    assert card["status"] == "paper_promotable"
    assert drift["downgrade"] is False
    assert vote["decision"] == "BUY"
    assert backlog["status"] == "clean"
    assert "never_enable_live_trading" in manual["chapters"]
