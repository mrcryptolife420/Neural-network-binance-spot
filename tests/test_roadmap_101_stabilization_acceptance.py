from __future__ import annotations

from pathlib import Path

from binance_spot_bot.check_reliability import check_reliability
from binance_spot_bot.dashboard_smoke_stabilizer import stabilize_dashboard_smoke
from binance_spot_bot.evidence_gap_detector import detect_evidence_gaps
from binance_spot_bot.flaky_check_burndown import detect_flaky_checks
from binance_spot_bot.paper_simulation_stabilizer import stabilize_paper_simulation
from binance_spot_bot.slow_check_hardening import detect_slow_checks
from binance_spot_bot.stabilization_audit_ingest import ingest_roadmap100_bundle, ingest_roadmap100_reports
from binance_spot_bot.stabilization_backlog import build_stabilization_backlog
from binance_spot_bot.stabilization_classifier import classify_stabilization_finding
from binance_spot_bot.stabilization_evidence_bundle import export_stabilization_evidence_bundle
from binance_spot_bot.stabilization_gate import evaluate_stabilization_gate
from binance_spot_bot.stabilization_report import build_stabilization_report
from binance_spot_bot.stabilization_secret_verify import verify_stabilization_secrets
from binance_spot_bot.stabilization_waivers import create_stabilization_waiver
from binance_spot_bot.stabilization_workplan import build_stabilization_workplans


def _write_roadmap100_artifacts(root: Path, *, no_live: bool = True) -> None:
    artifacts = {
        "data/milestone/reports/system_audit_report.json": '{"status": "ready", "live_trading_enabled": false}',
        "data/milestone/readiness/production_readiness_simulation.json": '{"status": "blocked", "live_trading_enabled": false}',
        "data/milestone/safety-invariants/system_safety_invariants.json": '{"status": "ok", "live_trading_enabled": false}',
        "data/milestone/paper-os-simulation/paper_os_simulation.json": '{"status": "ready", "live_trading_enabled": false}',
        "data/milestone/roadmap-traceability/roadmap_traceability_001_100.json": '{"status": "ok", "live_trading_enabled": false}',
    }
    if no_live:
        artifacts["data/milestone/no-live/no_live_proof_pack.json"] = '{"status": "ok", "live_trading_enabled": false, "signed_endpoints_used": false}'
    for relative, text in artifacts.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def test_ingest_missing_no_live_proof_creates_p0_finding(tmp_path: Path) -> None:
    _write_roadmap100_artifacts(tmp_path, no_live=False)
    report = ingest_roadmap100_reports(tmp_path)

    assert report["status"] == "blocked"
    assert any(finding["severity"] == "P0" and finding["source"]["name"] == "no_live_proof" for finding in report["findings"])
    assert report["live_trading_enabled"] is False
    assert report["no_live_statement"]


def test_bundle_ingest_requires_no_live_proof(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "milestone_bundle_manifest.json").write_text('{"files": [{"path": "files/system.json"}]}', encoding="utf-8")

    report = ingest_roadmap100_bundle(bundle)
    assert report["status"] == "blocked"
    assert report["findings"][0]["severity"] == "P0"


def test_classifier_backlog_workplan_and_gate_are_priority_aware() -> None:
    finding = {"title": "live mode found in dashboard", "category": "safety"}
    classified = classify_stabilization_finding(finding)
    backlog = build_stabilization_backlog([finding])
    workplans = build_stabilization_workplans(backlog, priority="P0")
    gate = evaluate_stabilization_gate(backlog)
    waiver = create_stabilization_waiver("STAB-001", priority="P0", reason="not allowed")

    assert classified["priority"] == "P0"
    assert backlog["status"] == "blocked"
    assert workplans["workplans"][0]["no_live_constraints"]
    assert gate["status"] == "blocked"
    assert waiver["status"] == "blocked"


def test_reliability_flaky_slow_dashboard_and_paper_stabilizers() -> None:
    history = [
        {"name": "dashboard-smoke", "status": "failed", "duration_ms": 250_000},
        {"name": "dashboard-smoke", "status": "ok", "duration_ms": 1000},
    ]
    reliability = check_reliability(history)
    flaky = detect_flaky_checks(history)
    slow = detect_slow_checks(history, budget_ms=180_000)
    dashboard = stabilize_dashboard_smoke([{"key": "paper_os", "live_trading_enabled": True}])
    paper = stabilize_paper_simulation(result={"status": "ready", "api_keys_required": True, "signed_endpoints_used": False})

    assert reliability["flaky_score"] == 1.0
    assert flaky["status"] == "warn"
    assert slow["status"] == "warn"
    assert dashboard["status"] == "blocked"
    assert paper["status"] == "blocked"


def test_evidence_gaps_secret_verify_report_and_bundle(tmp_path: Path) -> None:
    gaps = detect_evidence_gaps(["no_live_proof", "check_all"], ["check_all"])
    secret_file = tmp_path / "report.json"
    secret_file.write_text('{"api' + '_key": "' + ("a" * 32) + '"}', encoding="utf-8")
    secret_report = verify_stabilization_secrets([secret_file])
    ingest = {"status": "blocked", "findings": [{"title": "missing no-live", "category": "missing"}]}
    backlog = build_stabilization_backlog(ingest["findings"])
    gate = evaluate_stabilization_gate(backlog)
    report = build_stabilization_report(ingest, backlog, gate, gaps=gaps)
    bundle = export_stabilization_evidence_bundle([secret_file], tmp_path / "bundle")

    assert gaps["status"] == "blocked"
    assert secret_report["status"] == "blocked"
    assert report["status"] == "blocked"
    assert bundle["status"] == "ok"
    assert bundle["live_trading_enabled"] is False
