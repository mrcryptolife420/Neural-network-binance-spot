import json
import tempfile
from pathlib import Path

from binance_spot_bot.dashboard_v2.analytics_preset_packs import analytics_presets_payload
from binance_spot_bot.dashboard_v2.app import DashboardV2FallbackApp, create_dashboard_v2_app
from binance_spot_bot.dashboard_v2.extension_pack_evidence import export_extension_pack_evidence
from binance_spot_bot.dashboard_v2.extension_pack_registry import DashboardExtensionPackRegistry
from binance_spot_bot.dashboard_v2.extension_pack_schema import (
    DashboardExtensionPack,
    DashboardExtensionPackManifest,
    DashboardPackContent,
    dashboard_extension_pack_to_dict,
    finalized_extension_pack,
    validate_dashboard_extension_pack,
    write_dashboard_extension_pack,
)
from binance_spot_bot.dashboard_v2.pack_compatibility import evaluate_pack_compatibility
from binance_spot_bot.dashboard_v2.pack_install_preview import preview_pack_install
from binance_spot_bot.dashboard_v2.pack_migrations import migrate_pack_payload
from binance_spot_bot.dashboard_v2.pack_performance import evaluate_pack_performance
from binance_spot_bot.dashboard_v2.pack_recommendations import recommend_extension_packs
from binance_spot_bot.dashboard_v2.watchlist_packs import watchlist_packs_payload
from binance_spot_bot.dashboard_v2.workflow_packs import workflow_packs_payload
from binance_spot_bot.dashboard_v2.workspace_template_packs import build_template_pack, template_packs_payload
from binance_spot_bot.dashboard_v2.workspace_schema import dashboard_workspace_to_dict
from binance_spot_bot.dashboard_v2.workspace_presets import build_workspace_preset


def test_extension_pack_schema_blocks_live_code_remote_scripts_unknown_widgets_and_missing_safety():
    pack = build_template_pack("beginner_paper_operator")
    assert validate_dashboard_extension_pack(pack).status == "ok"
    assert dashboard_extension_pack_to_dict(pack)["manifest"]["live_trading_enabled"] is False

    bad = finalized_extension_pack(
        DashboardExtensionPack(
            manifest=DashboardExtensionPackManifest(
                pack_id="bad",
                name="Bad",
                description="https://example.invalid/download",
                version="1.0",
                pack_type="unknown",
                mode_scope="live",
                live_trading_enabled=True,
                required_widget_types=("live_order_button",),
            ),
            content=DashboardPackContent(docs="<script>alert(1)</script>", workflow_steps=({"code": "print(1)"},)),
        )
    )
    blockers = validate_dashboard_extension_pack(bad).blockers
    assert any("unknown pack_type" in item for item in blockers)
    assert any("live" in item for item in blockers)
    assert any("unknown widget" in item or "live widget" in item for item in blockers)
    assert any("unsafe script" in item for item in blockers)
    assert any("code execution" in item for item in blockers)
    assert any("remote URL" in item for item in blockers)

    unsafe_workspace = dashboard_workspace_to_dict(build_workspace_preset("operator_overview"))
    unsafe_workspace["layout"]["widgets"] = [widget for widget in unsafe_workspace["layout"]["widgets"] if widget["widget_type"] != "no_live_banner"]
    missing_safety = finalized_extension_pack(
        DashboardExtensionPack(
            manifest=DashboardExtensionPackManifest(
                pack_id="missing-safety",
                name="Missing Safety",
                description="Missing safety widget",
                version="1.0",
                pack_type="workspace_template",
            ),
            content=DashboardPackContent(workspace_templates=(unsafe_workspace,)),
        )
    )
    assert validate_dashboard_extension_pack(missing_safety).status == "blocked"


def test_pack_registry_preview_install_export_uninstall_and_secret_redaction():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        registry = DashboardExtensionPackRegistry(root / "packs")
        pack = build_template_pack("demo_spot_control_room")
        path = root / "pack.json"
        write_dashboard_extension_pack(path, pack)
        assert registry.available()["status"] == "ok"
        assert preview_pack_install(pack)["status"] == "ok"
        assert registry.install_file(path, confirm="")["status"] == "blocked"
        assert registry.install_file(path, confirm="INSTALL_LOCAL_PACK")["status"] == "ok"
        assert registry.set_enabled(pack.manifest.pack_id, True)["status"] == "ok"
        assert registry.validate_installed()["status"] == "ok"
        exported = registry.export(pack.manifest.pack_id)
        assert Path(exported["path"]).exists()
        assert registry.uninstall(pack.manifest.pack_id, confirm="UNINSTALL_LOCAL_PACK")["status"] == "ok"

        payload = dashboard_extension_pack_to_dict(pack)
        payload["content"]["docs"] = "api_key=" + ("B" * 56)
        secret_path = root / "secret-pack.json"
        secret_path.write_text(json.dumps(payload), encoding="utf-8")
        loaded_text = secret_path.read_text(encoding="utf-8")
        assert "B" * 56 in loaded_text
        secret_pack = DashboardExtensionPack(
            manifest=DashboardExtensionPackManifest(pack_id="secret-pack", name="Secret Pack", description="Secret test", version="1.0", pack_type="workspace_template"),
            content=DashboardPackContent(docs="api_key=" + ("C" * 56)),
        )
        assert validate_dashboard_extension_pack(secret_pack).status == "blocked"
        redacted_pack = finalized_extension_pack(secret_pack)
        assert "C" * 56 not in json.dumps(dashboard_extension_pack_to_dict(redacted_pack))


def test_template_analytics_watchlist_workflow_recommendations_compatibility_performance_evidence_and_migration():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        assert template_packs_payload()["status"] == "ok"
        assert analytics_presets_payload()["status"] == "ok"
        assert watchlist_packs_payload()["status"] == "ok"
        assert workflow_packs_payload()["status"] == "ok"
        pack = build_template_pack("model_monitoring_desk")
        assert evaluate_pack_compatibility(pack)["status"] == "compatible"
        assert evaluate_pack_performance(pack)["status"] == "ok"
        assert recommend_extension_packs({"workflow": "model-review"})["recommended_template_pack"] == "model_monitoring_desk"
        migrated = migrate_pack_payload(dashboard_extension_pack_to_dict(pack))
        assert migrated["manifest"]["schema_version"] == 2
        evidence = export_extension_pack_evidence(root)
        assert evidence["status"] == "ok"
        manifest = Path(evidence["manifest"]).read_text(encoding="utf-8")
        assert "live_trading_enabled" in manifest


def test_extension_pack_api_fallback_and_fastapi_routes_are_no_live():
    fallback = DashboardV2FallbackApp()
    assert fallback.extension_packs()["live_trading_enabled"] is False
    app = create_dashboard_v2_app()
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    if isinstance(app, DashboardV2FallbackApp):
        return
    client = TestClient(app)
    assert client.get("/api/extension-packs").json()["live_trading_enabled"] is False
    assert client.get("/api/extension-packs/recommendations").json()["status"] == "ok"
