from __future__ import annotations

import json

from binance_spot_bot.dashboard_v2.cli_router import dashboard_v2_cli_router_report
from binance_spot_bot.dashboard_v2.critical_workflow_lock import dashboard_v2_critical_workflow_lock
from binance_spot_bot.dashboard_v2.deprecation_evidence_bundle import export_dashboard_v2_deprecation_evidence_bundle
from binance_spot_bot.dashboard_v2.deprecation_gate import dashboard_v2_deprecation_gate
from binance_spot_bot.dashboard_v2.fallback_drill import dashboard_v2_fallback_drill
from binance_spot_bot.dashboard_v2.final_parity_lock import build_dashboard_final_parity_lock, write_dashboard_final_parity_lock
from binance_spot_bot.dashboard_v2.legacy_compat import dashboard_v2_legacy_compat_map
from binance_spot_bot.dashboard_v2.operator_mode import dashboard_v2_operator_mode_smoke
from binance_spot_bot.dashboard_v2.streamlit_change_freeze import dashboard_v2_streamlit_change_freeze
from binance_spot_bot.dashboard_v2.streamlit_only_inventory import dashboard_v2_streamlit_only_inventory
from binance_spot_bot.dashboard_v2.v2_first_checks import dashboard_v2_docs_v2_first_check, dashboard_v2_uat_v2_first_check
from binance_spot_bot.dashboard_v2.v2_only_smoke import dashboard_v2_only_smoke
from binance_spot_bot.ui.page_registry import PAGES


def test_final_parity_lock_covers_all_pages_and_is_no_live(tmp_path):
    report = build_dashboard_final_parity_lock(tmp_path).to_dict()
    written = write_dashboard_final_parity_lock(tmp_path)

    assert report["status"] == "ok"
    assert len(report["lock"]["items"]) == len(PAGES)
    assert report["hard_blockers"] == []
    assert report["lock"]["live_trading_enabled"] is False
    assert "NO LIVE TRADING" in report["lock"]["no_live_statement"]
    assert written["live_trading_enabled"] is False


def test_streamlit_inventory_workflows_router_operator_mode_and_compat_are_safe(tmp_path):
    inventory = dashboard_v2_streamlit_only_inventory(tmp_path)
    workflows = dashboard_v2_critical_workflow_lock()
    router = dashboard_v2_cli_router_report()
    operator = dashboard_v2_operator_mode_smoke()
    compat = dashboard_v2_legacy_compat_map()
    freeze = dashboard_v2_streamlit_change_freeze(tmp_path)

    assert inventory["streamlit_only_pages"] == []
    assert all(item["status"] == "locked" for item in workflows["workflows"])
    assert router["v2_first"] is True
    assert operator["streamlit_import_required"] is False
    assert len(compat["mappings"]) == len(PAGES)
    assert freeze["waiver_required_for_streamlit_only"] is True


def test_deprecation_gate_v2_only_smoke_fallback_and_docs_uat():
    docs = dashboard_v2_docs_v2_first_check()
    uat = dashboard_v2_uat_v2_first_check()
    gate = dashboard_v2_deprecation_gate()
    smoke = dashboard_v2_only_smoke()
    drill = dashboard_v2_fallback_drill()

    assert docs["status"] == "ok"
    assert uat["status"] == "ok"
    assert gate["status"] == "deprecation_candidate"
    assert gate["streamlit_removed"] is False
    assert smoke["streamlit_imported"] is False
    assert "--legacy-streamlit" in drill["fallback_command"]


def test_deprecation_evidence_bundle_is_secret_free(tmp_path):
    evidence = export_dashboard_v2_deprecation_evidence_bundle(tmp_path)
    text = json.dumps(evidence)

    assert evidence["status"] == "ok"
    assert evidence["live_trading_enabled"] is False
    assert "streamlit_deprecation_evidence_manifest.json" in evidence["manifest"]
    assert "api_key" not in text.lower()
    assert (tmp_path / "data" / "dashboard-v2" / "deprecation" / "evidence" / evidence["run_id"] / "streamlit_deprecation_evidence_manifest.json").exists()
