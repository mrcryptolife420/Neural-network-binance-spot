from __future__ import annotations

import json
from pathlib import Path

from binance_spot_bot.dashboard_walkthroughs import build_dashboard_walkthroughs
from binance_spot_bot.evidence_interpreter import interpret_evidence
from binance_spot_bot.no_live_training import no_live_training_lesson
from binance_spot_bot.operator_certification import certification_draft, complete_certification
from binance_spot_bot.operator_cli_cookbook import operator_cli_cookbook
from binance_spot_bot.operator_docs_consistency import check_operator_docs_consistency
from binance_spot_bot.operator_docs_index import build_operator_docs_index, operator_docs_index_to_dict, validate_operator_docs_index
from binance_spot_bot.operator_glossary import explain_operator_term, operator_glossary
from binance_spot_bot.operator_training import build_training_lessons
from binance_spot_bot.operator_training_evidence import export_operator_training_evidence
from binance_spot_bot.operator_training_store import save_training_progress
from binance_spot_bot.support_bundle_interpreter import interpret_support_bundle_manifest
from binance_spot_bot.training_scenarios import list_training_scenarios, run_training_scenario
from binance_spot_bot.troubleshooting_playbooks import troubleshooting_playbooks


def _docs(root: Path, text: str = "# Operator\n\nLive trading: disabled.\n") -> None:
    (root / "docs" / "operator").mkdir(parents=True)
    (root / "docs" / "operator" / "index.md").write_text(text, encoding="utf-8")


def test_operator_docs_index_validates_no_live_and_forbidden_phrases(tmp_path: Path) -> None:
    _docs(tmp_path)
    index = build_operator_docs_index(tmp_path)
    payload = operator_docs_index_to_dict(index)
    validation = validate_operator_docs_index(index)

    assert payload["live_trading_enabled"] is False
    assert validation.status == "ok"
    json.dumps(payload)

    (tmp_path / "docs" / "operator" / "index.md").write_text("# Bad\n\nlive approved\n", encoding="utf-8")
    blocked = validate_operator_docs_index(build_operator_docs_index(tmp_path))
    assert blocked.status == "blocked"


def test_cli_cookbook_walkthroughs_lessons_scenarios_and_playbooks_are_paper_only() -> None:
    cookbook = operator_cli_cookbook()
    walkthroughs = build_dashboard_walkthroughs(["overview", "paper_os_audit"])
    lessons = build_training_lessons()
    scenarios = list_training_scenarios()
    scenario = run_training_scenario("scenario-003-paper-session-smoke")
    playbooks = troubleshooting_playbooks()

    assert all(command["live_trading_enabled"] is False for command in cookbook["commands"])
    assert len(walkthroughs["walkthroughs"]) == 2
    assert lessons["lessons"][0]["no_live_banner"] == "OPERATOR TRAINING - NO LIVE TRADING"
    assert scenario["status"] == "ready"
    assert scenarios["scenarios"]
    assert playbooks["playbooks"][0]["no_live_constraints"]


def test_support_evidence_glossary_no_live_and_certification_contracts(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"files": [{"path": "report.json"}]}', encoding="utf-8")
    support = interpret_support_bundle_manifest(manifest)
    evidence = interpret_evidence(["missing:no_live_proof"])
    glossary = operator_glossary()
    term = explain_operator_term("kill switch")
    lesson = no_live_training_lesson()
    failed_lesson = no_live_training_lesson(failure_example=True)
    draft = certification_draft("paper-operator")
    blocked = complete_certification("paper-operator", "LIVE")
    passed = complete_certification("paper-operator", "PAPER_ONLY_CERTIFICATION")

    assert support["status"] == "ok"
    assert evidence["status"] == "warn"
    assert glossary["terms"]["live"] == "disabled"
    assert "safety" in term["meaning"]
    assert lesson["status"] == "ok"
    assert failed_lesson["status"] == "blocked"
    assert draft["approval_scope"] == "paper_only"
    assert blocked["status"] == "blocked"
    assert passed["status"] == "passed"


def test_training_store_evidence_and_docs_consistency(tmp_path: Path) -> None:
    saved = save_training_progress(tmp_path, "operator", "lesson-no-live", "complete")
    consistency = check_operator_docs_consistency(["Live trading: disabled."], ["validate-config"])
    blocked = check_operator_docs_consistency(["live approved"], ["validate-config"])
    evidence = export_operator_training_evidence([Path(saved["path"])], tmp_path / "bundle")

    assert Path(saved["path"]).exists()
    assert consistency["status"] == "ok"
    assert blocked["status"] == "blocked"
    assert evidence["status"] == "ok"
    assert evidence["live_trading_enabled"] is False
