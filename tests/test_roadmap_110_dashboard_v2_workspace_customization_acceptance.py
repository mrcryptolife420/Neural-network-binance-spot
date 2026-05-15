import json
import tempfile
from pathlib import Path

from binance_spot_bot.dashboard_v2.advanced_analytics import advanced_analytics_report
from binance_spot_bot.dashboard_v2.analytics_query import analytics_query
from binance_spot_bot.dashboard_v2.app import DashboardV2FallbackApp, create_dashboard_v2_app
from binance_spot_bot.dashboard_v2.chart_sync import compare_chart_sessions, create_chart_sync_state
from binance_spot_bot.dashboard_v2.operator_preferences import DashboardV2OperatorPreferences, validate_operator_preferences
from binance_spot_bot.dashboard_v2.watchlists import default_watchlist_store
from binance_spot_bot.dashboard_v2.widget_registry import validate_widget_registry, validate_widget_types, widget_registry_payload
from binance_spot_bot.dashboard_v2.workspace_evidence_bundle import export_workspace_evidence_bundle
from binance_spot_bot.dashboard_v2.workspace_migrations import migrate_workspace_payload
from binance_spot_bot.dashboard_v2.workspace_performance import evaluate_workspace_performance
from binance_spot_bot.dashboard_v2.workspace_presets import PRESET_WIDGETS, build_workspace_preset, workspace_presets_payload
from binance_spot_bot.dashboard_v2.workspace_schema import (
    DashboardWorkspace,
    DashboardWorkspaceLayout,
    DashboardWorkspacePanel,
    DashboardWorkspaceWidget,
    dashboard_workspace_from_dict,
    dashboard_workspace_to_dict,
    validate_dashboard_workspace,
)
from binance_spot_bot.dashboard_v2.workspace_store import DashboardWorkspaceStore


def test_workspace_schema_blocks_live_and_requires_locked_safety_widgets():
    valid = build_workspace_preset("operator_overview")
    assert validate_dashboard_workspace(valid).status == "ok"
    payload = dashboard_workspace_to_dict(valid)
    assert payload["live_trading_enabled"] is False
    assert payload["no_live_statement"]
    assert dashboard_workspace_from_dict(payload).workspace_id == valid.workspace_id

    live = DashboardWorkspace(
        workspace_id="bad-live",
        name="Bad",
        mode_scope="live",
        live_trading_enabled=True,
        layout=valid.layout,
    )
    result = validate_dashboard_workspace(live)
    assert result.status == "blocked"
    assert any("live" in blocker for blocker in result.blockers)

    unlocked = DashboardWorkspace(
        workspace_id="bad-safety",
        name="Bad Safety",
        safety_widgets_locked=False,
        layout=valid.layout,
    )
    assert validate_dashboard_workspace(unlocked).status == "blocked"


def test_workspace_schema_blocks_duplicates_missing_refs_dimensions_scripts_and_secret_settings():
    widgets = (
        DashboardWorkspaceWidget("safe1", "no_live_banner", "No Live", locked=True),
        DashboardWorkspaceWidget("stop1", "stop_button", "Stop", locked=True),
        DashboardWorkspaceWidget("dup", "runtime_status", "Runtime", settings={"note": "<script>alert(1)</script>"}),
        DashboardWorkspaceWidget("dup", "runtime_status", "Runtime Again"),
    )
    workspace = DashboardWorkspace(
        workspace_id="invalid-workspace",
        name="Invalid",
        layout=DashboardWorkspaceLayout(
            widgets=widgets,
            panels=(
                DashboardWorkspacePanel("panel1", "Panel", 0, 0, 0, 2, "safe1"),
                DashboardWorkspacePanel("panel1", "Panel", 0, 0, 2, 2, "missing"),
            ),
        ),
    )
    blockers = validate_dashboard_workspace(workspace).blockers
    assert any("duplicate widget_id" in item for item in blockers)
    assert any("duplicate panel_id" in item for item in blockers)
    assert any("missing widget_id" in item for item in blockers)
    assert any("invalid dimensions" in item for item in blockers)
    assert any("unsafe script" in item for item in blockers)


def test_widget_registry_and_presets_are_allowlisted_and_no_live():
    registry = widget_registry_payload()
    assert registry["status"] == "ok"
    assert validate_widget_registry()["status"] == "ok"
    assert validate_widget_types(["candle_chart", "live_order_button"])["status"] == "blocked"
    presets = workspace_presets_payload()
    assert presets["status"] == "ok"
    assert {item["preset_id"] for item in presets["presets"]} == set(PRESET_WIDGETS)


def test_workspace_store_clone_export_import_hashes_and_redaction():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = DashboardWorkspaceStore(root / "workspaces")
        workspace = build_workspace_preset("operator_overview", name="My Workspace")
        saved = store.save(workspace)
        assert saved["status"] == "ok"
        assert store.list()["count"] == 1
        assert store.verify_hashes()["status"] == "ok"
        assert store.clone(workspace.workspace_id)["status"] == "ok"
        exported = store.export(workspace.workspace_id)
        text = Path(exported["path"]).read_text(encoding="utf-8")
        assert "LOCAL REALTIME DASHBOARD" in text
        payload = json.loads(text)
        payload["workspace_id"] = "imported-workspace"
        payload["layout"]["widgets"][2]["settings"]["api_key"] = "A" * 56
        import_path = root / "import.json"
        import_path.write_text(json.dumps(payload), encoding="utf-8")
        imported = store.import_workspace(import_path, dry_run=False)
        assert imported["status"] == "ok"
        imported_text = (store.layouts_dir / "imported-workspace.json").read_text(encoding="utf-8")
        assert "A" * 56 not in imported_text
        assert "[REDACTED]" in imported_text


def test_analytics_watchlists_preferences_chart_sync_migrations_performance_and_evidence():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        workspace = build_workspace_preset("operator_overview")
        store = DashboardWorkspaceStore(root / "data" / "dashboard-v2" / "workspaces")
        store.save(workspace)

        assert analytics_query(scope="candles", tail=3)["payload_bytes"] > 0
        assert analytics_query(scope="runtime_snapshot", mode="live")["status"] == "blocked"
        assert advanced_analytics_report()["status"] == "ok"
        assert create_chart_sync_state(workspace.workspace_id)["status"] == "ok"
        assert compare_chart_sessions([{"x": 1}], [])["delta_points"] == 1
        assert evaluate_workspace_performance(workspace)["status"] == "ok"

        watchlists = default_watchlist_store(root)
        assert watchlists.create("Majors", ["BTCUSDT", "ETHUSDT"])["status"] == "ok"
        assert watchlists.create("Bad", ["bad-symbol!"])["status"] == "blocked"
        assert validate_operator_preferences(DashboardV2OperatorPreferences(default_mode="live"))["status"] == "blocked"

        v1 = dashboard_workspace_to_dict(workspace)
        v1.pop("metadata")
        migrated = migrate_workspace_payload(v1)
        assert migrated["metadata"]["schema_version"] == 2

        evidence = export_workspace_evidence_bundle(root, workspace.workspace_id)
        assert evidence["status"] == "ok"
        manifest = Path(evidence["manifest"]).read_text(encoding="utf-8")
        assert "live_trading_enabled" in manifest


def test_workspace_api_fallback_and_fastapi_routes_expose_no_live_surfaces():
    fallback = DashboardV2FallbackApp()
    assert fallback.widgets()["status"] == "ok"
    assert fallback.workspace_presets()["status"] == "ok"
    assert fallback.analytics_query()["live_trading_enabled"] is False

    app = create_dashboard_v2_app()
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    if isinstance(app, DashboardV2FallbackApp):
        return
    client = TestClient(app)
    assert client.get("/api/widgets").json()["live_trading_enabled"] is False
    assert client.get("/api/workspace-presets").json()["status"] == "ok"
    assert client.get("/api/analytics/query?scope=runtime_snapshot").json()["live_trading_enabled"] is False
