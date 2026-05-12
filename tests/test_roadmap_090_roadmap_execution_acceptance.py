from pathlib import Path

from binance_spot_bot.codex_task_pack_generator import generate_codex_task_packs
from binance_spot_bot.codex_task_packs import validate_task_pack_no_live
from binance_spot_bot.pr_template_generator import generate_pr_template
from binance_spot_bot.roadmap_completion_gate import evaluate_roadmap_completion_gate
from binance_spot_bot.roadmap_dependency_graph import build_roadmap_dependency_graph
from binance_spot_bot.roadmap_duplicate_guard import run_roadmap_duplicate_guard
from binance_spot_bot.roadmap_evidence_bundle import export_roadmap_evidence_bundle, verify_roadmap_evidence_bundle
from binance_spot_bot.roadmap_execution_report import build_roadmap_execution_report, write_roadmap_execution_report
from binance_spot_bot.roadmap_index import build_roadmap_index, find_next_roadmap_number
from binance_spot_bot.roadmap_mover import move_completed_roadmap
from binance_spot_bot.roadmap_quality_score import roadmap_quality_score
from binance_spot_bot.roadmap_release_integration import generate_roadmap_release_input
from binance_spot_bot.roadmap_validation import validate_roadmap_file


def _write_fixture(root: Path) -> Path:
    open_dir = root / "Roadmap docs"
    done_dir = root / "Voltooid docs"
    open_dir.mkdir()
    done_dir.mkdir()
    (done_dir / "089-roadmap-release.md").write_text(
        "# Roadmap 089 - Release\n\nStatus: Voltooid\n\n## Definition of Done\n\nAcceptatiecriteria:\n- [x] done\n\nGeen live trading.\n",
        encoding="utf-8",
    )
    roadmap = open_dir / "090-roadmap-execution.md"
    roadmap.write_text(
        "# Roadmap 090 - Execution\n\n"
        "Status: In uitvoering\n\n"
        "Volgt op: Voltooid docs/089-roadmap-release.md\n\n"
        "## Fase 1\n\nAcceptatiecriteria:\n- [ ] tests\n\n"
        "## Tests\n\n`tests/test_roadmap_090_roadmap_execution_acceptance.py`\n\n"
        "## Docs\n\n`docs/roadmap-execution-cli.md`\n\n"
        "## Definition of Done\n\nGeen live trading. Beste eerste Codex-opdracht.\n"
        "`src/binance_spot_bot/roadmap_index.py`\n",
        encoding="utf-8",
    )
    return roadmap


def test_roadmap_index_duplicate_validation_and_quality(tmp_path: Path):
    roadmap = _write_fixture(tmp_path)
    index = build_roadmap_index(tmp_path)
    assert index["payload"]["open_count"] == 1
    assert index["payload"]["done_count"] == 1
    assert find_next_roadmap_number(index) == 91
    guard = run_roadmap_duplicate_guard(tmp_path, number=90)
    assert guard["status"] == "blocked"
    assert "number_already_exists:090" in guard["blockers"]
    validation = validate_roadmap_file(roadmap, tmp_path)
    assert validation["status"] == "ok"
    score = roadmap_quality_score(roadmap.read_text(encoding="utf-8"))
    assert score["grade"] in {"A", "B"}
    assert score["live_trading_enabled"] is False


def test_task_packs_pr_templates_graph_and_release_input(tmp_path: Path):
    _write_fixture(tmp_path)
    graph = build_roadmap_dependency_graph(tmp_path)
    assert graph["summary"]["roadmaps"] == 2
    pack = generate_codex_task_packs(tmp_path, "090")
    assert pack["status"] == "ready"
    assert validate_task_pack_no_live(pack)["status"] == "ok"
    assert list((tmp_path / "data" / "roadmaps" / "task-packs" / "090").glob("pr-*-task-pack.json"))
    template = generate_pr_template("090", "foundation")
    assert "No live trading" in template["markdown"]
    release_input = generate_roadmap_release_input(tmp_path)
    assert release_input["status"] == "ready"


def test_completion_gate_mover_and_evidence_bundle(tmp_path: Path):
    roadmap = _write_fixture(tmp_path)
    blocked = evaluate_roadmap_completion_gate("090", evidence={"tests_passed": True, "check_all_passed": False, "no_live_proof": True})
    assert blocked["status"] == "needs_evidence"
    ready_evidence = {"tests_passed": True, "check_all_passed": True, "no_live_proof": True}
    ready = evaluate_roadmap_completion_gate("090", evidence=ready_evidence)
    assert ready["status"] == "ready_to_complete"
    dry_run = move_completed_roadmap(tmp_path, "090", evidence=ready_evidence, dry_run=True)
    assert dry_run["status"] == "dry_run"
    moved = move_completed_roadmap(tmp_path, "090", confirm="MOVE_ROADMAP_TO_VOLTOOID", evidence=ready_evidence, dry_run=False)
    assert moved["status"] == "moved"
    assert not roadmap.exists()
    bundle = export_roadmap_evidence_bundle([tmp_path / "Voltooid docs" / "090-roadmap-execution.md"], tmp_path / "evidence")
    assert verify_roadmap_evidence_bundle(bundle["manifest"])["status"] == "ok"


def test_execution_report_writes_outputs(tmp_path: Path):
    _write_fixture(tmp_path)
    report = build_roadmap_execution_report(tmp_path)
    paths = write_roadmap_execution_report(tmp_path, report)
    assert report["live_trading_enabled"] is False
    assert Path(paths["json"]).exists()
    assert Path(paths["markdown"]).exists()
