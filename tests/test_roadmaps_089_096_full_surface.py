from __future__ import annotations

from binance_spot_bot.check_all_v2 import check_all_v2
from binance_spot_bot.code_graph import code_graph
from binance_spot_bot.dashboard_smoke_v2 import dashboard_smoke_v2
from binance_spot_bot.data_quality_v2 import data_quality_v2
from binance_spot_bot.impact_analysis import impact_analysis
from binance_spot_bot.indicator_compute import compute_indicator
from binance_spot_bot.intelligent_test_selector import selected_tests
from binance_spot_bot.migration_apply import migration_apply
from binance_spot_bot.performance_budget import performance_budget
from binance_spot_bot.release_manifest import release_manifest
from binance_spot_bot.roadmap_completion_gate import roadmap_completion_gate
from binance_spot_bot.roadmap_duplicate_guard import roadmap_duplicate_guard
from binance_spot_bot.runtime_event_bus import RuntimeEventBus
from binance_spot_bot.runtime_snapshot_builder import build_runtime_snapshot
from binance_spot_bot.runtime_snapshot_limits import enforce_snapshot_limits
from binance_spot_bot.versioning import version_payload


def test_089_release_management_blocks_unconfirmed_migration(tmp_path):
    version = version_payload("1.2.3")
    manifest = release_manifest(tmp_path, "1.2.3")
    blocked = migration_apply("demo", confirm="")
    applied = migration_apply("demo", confirm="APPLY_LOCAL_MIGRATION")

    assert version["payload"]["version"] == "1.2.3"
    assert manifest["live_trading_enabled"] is False
    assert blocked["status"] == "blocked"
    assert applied["status"] == "applied"


def test_090_roadmap_execution_guards_duplicates_and_completion():
    duplicates = roadmap_duplicate_guard(["a", "b", "a"])
    gate = roadmap_completion_gate(tests_ok=True, evidence_present=True)

    assert duplicates["status"] == "blocked"
    assert gate["status"] == "ok"
    assert gate["live_trading_enabled"] is False


def test_091_repo_knowledge_graph_and_impact(tmp_path):
    src = tmp_path / "src" / "binance_spot_bot"
    src.mkdir(parents=True)
    (src / "a.py").write_text("from . import b\n", encoding="utf-8")

    graph = code_graph(tmp_path)
    impact = impact_analysis(["src/binance_spot_bot/runtime.py"])

    assert graph["payload"]["nodes"] == ["a.py"]
    assert impact["risk"]["payload"]["score"] >= 40
    assert impact["live_trading_enabled"] is False


def test_092_intelligent_test_selection_selects_risk_tests():
    selection = selected_tests(["src/binance_spot_bot/security.py"])
    check = check_all_v2(["src/binance_spot_bot/ui/streamlit_app.py"])

    assert "tests/test_risk_execution_security.py" in selection["payload"]["tests"]
    assert check["status"] == "ok"
    assert check["live_trading_enabled"] is False


def test_093_performance_budget_warns_on_regression():
    ok = performance_budget(10, 20)
    warn = performance_budget(30, 20)

    assert ok["status"] == "ok"
    assert warn["status"] == "warn"
    assert warn["live_trading_enabled"] is False


def test_094_dashboard_smoke_v2_surface():
    smoke = dashboard_smoke_v2()

    assert smoke["payload"]["stable_keys"] is True
    assert smoke["payload"]["lazy_sections"] is True
    assert smoke["live_trading_enabled"] is False


def test_095_runtime_event_bus_and_snapshot_limits():
    bus = RuntimeEventBus()
    event = {"type": "tick"}
    published = bus.publish(event)
    snapshot = build_runtime_snapshot({"a": 1, "b": 2})
    limited = enforce_snapshot_limits({"a": 1, "b": 2}, max_items=1)

    assert published["status"] == "published"
    assert bus.drain() == [event]
    assert snapshot["kind"] == "runtime_snapshot"
    assert list(limited["limited"].keys()) == ["a"]


def test_096_data_pipeline_contracts_indicator_compute():
    quality = data_quality_v2([{"close": 1}])
    indicator = compute_indicator([1.0, 2.0, 3.0])

    assert quality["status"] == "ok"
    assert indicator["value"] == 2.0
    assert indicator["live_trading_enabled"] is False
