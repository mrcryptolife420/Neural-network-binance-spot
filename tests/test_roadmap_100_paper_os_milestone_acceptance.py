from __future__ import annotations

import json
from pathlib import Path

from binance_spot_bot.milestone_bundle import export_milestone_bundle
from binance_spot_bot.milestone_profiles import get_milestone_profile, milestone_profiles
from binance_spot_bot.milestone_runner import run_milestone_profile
from binance_spot_bot.milestone_verification import verify_milestone_bundle
from binance_spot_bot.no_live_proof_pack import build_no_live_proof_pack
from binance_spot_bot.operator_signoff import approve_operator_signoff, operator_signoff_draft
from binance_spot_bot.paper_os_readiness_score import calculate_paper_os_readiness_score
from binance_spot_bot.paper_os_simulation import build_paper_os_simulation
from binance_spot_bot.production_readiness_simulation import build_production_readiness_simulation
from binance_spot_bot.roadmap_milestone_traceability import build_roadmap_milestone_traceability
from binance_spot_bot.system_audit_report import build_system_audit_report
from binance_spot_bot.system_inventory import build_system_inventory, system_inventory_to_dict
from binance_spot_bot.system_safety_invariants import audit_system_safety_invariants, command_is_allowed_for_milestone


def _fixture_repo(root: Path) -> None:
    (root / "src" / "binance_spot_bot" / "ui").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "docs").mkdir()
    (root / "Roadmap docs").mkdir()
    for module in [
        "config.py",
        "preflight.py",
        "security.py",
        "runtime.py",
        "check_all.py",
        "milestone_runner.py",
    ]:
        (root / "src" / "binance_spot_bot" / module).write_text("LIVE_TRADING_ENABLED=false\norder account live\n", encoding="utf-8")
    (root / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").write_text("NO LIVE TRADING\n", encoding="utf-8")
    (root / "Roadmap docs" / "100-roadmap.md").write_text("# Roadmap\n\n## Definition of Done\n", encoding="utf-8")
    (root / "tests" / "test_100_demo.py").write_text("def test_demo(): pass\n", encoding="utf-8")
    (root / "docs" / "system-inventory.md").write_text("# docs\n", encoding="utf-8")


def test_system_inventory_is_offline_serializable_and_paper_only(tmp_path: Path) -> None:
    _fixture_repo(tmp_path)
    report = build_system_inventory(tmp_path)
    payload = system_inventory_to_dict(report)

    assert payload["live_trading_enabled"] is False
    assert payload["no_live_statement"]
    assert payload["subsystems"]
    assert any(row["name"] == "config/preflight/security" for row in payload["subsystems"])
    json.dumps(payload)


def test_safety_invariants_fail_live_mode_fixture_and_allow_paper_modes(tmp_path: Path) -> None:
    _fixture_repo(tmp_path)
    ok = audit_system_safety_invariants(tmp_path, selectable_modes=["demo", "paper", "testnet-readiness"])
    blocked = audit_system_safety_invariants(tmp_path, selectable_modes=["demo", "live"])

    assert ok["status"] == "ok"
    assert blocked["status"] == "blocked"
    assert "live mode not selectable" in blocked["hard_failures"]


def test_milestone_profiles_and_runner_enforce_safe_commands_and_confirm(tmp_path: Path) -> None:
    profiles = milestone_profiles()
    standard = get_milestone_profile("standard_milestone")
    blocked = run_milestone_profile("standard_milestone", root=tmp_path)
    ok = run_milestone_profile("standard_milestone", confirm=standard.confirm_phrase, root=tmp_path)

    assert profiles["live_trading_enabled"] is False
    assert blocked["status"] == "blocked"
    assert ok["status"] == "ok"
    assert command_is_allowed_for_milestone("system-inventory")
    assert not command_is_allowed_for_milestone("live-order place")


def test_paper_os_simulation_readiness_no_live_and_traceability(tmp_path: Path) -> None:
    _fixture_repo(tmp_path)
    simulation = build_paper_os_simulation(tmp_path)
    readiness = build_production_readiness_simulation(tmp_path)
    proof = build_no_live_proof_pack(tmp_path)
    traceability = build_roadmap_milestone_traceability(tmp_path, 100, 100)

    assert simulation["payload"]["status"] == "ready"
    assert simulation["live_trading_enabled"] is False
    assert readiness["status"] == "blocked"
    assert readiness["live_trading_enabled"] is False
    assert proof["signed_endpoints_used"] is False
    assert "100" in traceability["roadmaps"]


def test_readiness_score_hard_failure_signoff_and_audit_report(tmp_path: Path) -> None:
    _fixture_repo(tmp_path)
    score = calculate_paper_os_readiness_score(
        [
            {"name": "no_live", "category": "safety", "status": "blocked", "hard_fail": True},
            {"name": "tests", "category": "tests", "status": "ok"},
        ]
    )
    draft = operator_signoff_draft()
    signed = approve_operator_signoff("PAPER_OS_SIGNOFF")
    live_wording = approve_operator_signoff("PAPER_OS_SIGNOFF", notes="approve live trading")
    audit = build_system_audit_report(tmp_path)

    assert score["grade"] == "F"
    assert draft["status"] == "draft"
    assert signed["status"] == "signed"
    assert live_wording["status"] == "blocked"
    assert audit["live_trading_enabled"] is False


def test_milestone_bundle_verification_requires_no_live_proof(tmp_path: Path) -> None:
    proof = tmp_path / "no_live_proof_pack.json"
    proof.write_text('{"status": "ok", "live_trading_enabled": false}', encoding="utf-8")
    extra = tmp_path / "system_inventory.json"
    extra.write_text('{"status": "ok"}', encoding="utf-8")
    bundle = tmp_path / "bundle"
    export_milestone_bundle([proof, extra], bundle)

    verified = verify_milestone_bundle(bundle)
    assert verified["status"] == "ok"
    assert verified["no_live_proof_present"] is True

    (bundle / "files" / "system_inventory.json").write_text("tampered", encoding="utf-8")
    tampered = verify_milestone_bundle(bundle)
    assert tampered["status"] == "blocked"
