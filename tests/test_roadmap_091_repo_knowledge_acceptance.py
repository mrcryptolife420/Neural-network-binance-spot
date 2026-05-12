from pathlib import Path

from binance_spot_bot.artifact_flow_graph import build_artifact_flow_graph
from binance_spot_bot.cli_surface_map import build_cli_surface_map
from binance_spot_bot.code_graph import build_code_graph
from binance_spot_bot.code_ownership import build_code_ownership
from binance_spot_bot.dashboard_surface_map import build_dashboard_surface_map
from binance_spot_bot.docs_code_consistency import docs_code_consistency
from binance_spot_bot.impact_analysis import impact_analysis
from binance_spot_bot.refactor_candidates import detect_refactor_candidates
from binance_spot_bot.repo_inventory import build_repo_inventory, verify_repo_inventory_manifest, write_repo_inventory_manifest
from binance_spot_bot.repo_knowledge_codex_integration import repo_knowledge_codex_task_hints
from binance_spot_bot.repo_knowledge_report import build_repo_knowledge_report, write_repo_knowledge_report
from binance_spot_bot.repo_knowledge_store import verify_repo_knowledge_store, write_repo_knowledge_store
from binance_spot_bot.roadmap_traceability import build_roadmap_traceability
from binance_spot_bot.safety_surface_map import safety_surface_map
from binance_spot_bot.test_impact_map import select_tests_for_changes


def _fixture_repo(root: Path) -> None:
    src = root / "src" / "binance_spot_bot"
    tests = root / "tests"
    docs = root / "docs"
    roadmaps = root / "Roadmap docs"
    done = root / "Voltooid docs"
    for directory in [src / "ui", tests, docs, roadmaps, done]:
        directory.mkdir(parents=True, exist_ok=True)
    (src / "__init__.py").write_text("", encoding="utf-8")
    (src / "runtime.py").write_text("from .risk import RiskEngine\nclass Runtime: pass\ndef run(): pass\n", encoding="utf-8")
    (src / "risk.py").write_text("class RiskEngine: pass\n", encoding="utf-8")
    (src / "cli.py").write_text('sub.add_parser("check-all")\nsub.add_parser("dashboard-smoke")\n', encoding="utf-8")
    (src / "ui" / "streamlit_app.py").write_text('def _render_overview(): pass\nst.subheader("Overview")\n', encoding="utf-8")
    (tests / "test_runtime.py").write_text("from binance_spot_bot.runtime import Runtime\n", encoding="utf-8")
    (docs / "impact-analysis.md").write_text("check-all\n\nLive trading enabled: false\n", encoding="utf-8")
    (roadmaps / "091-roadmap-repo-knowledge.md").write_text(
        "# Roadmap 091 - Repo Knowledge\n\nStatus: Open\n\nVolgt op: Voltooid docs/090-roadmap.md\n\n"
        "`src/binance_spot_bot/runtime.py`\n`tests/test_runtime.py`\n`docs/impact-analysis.md`\n\n"
        "## Definition of Done\n\nAcceptatiecriteria:\n- [ ] done\n\nGeen live trading.\n",
        encoding="utf-8",
    )
    (done / "090-roadmap.md").write_text("# Roadmap 090 - Done\n\nStatus: Voltooid\n", encoding="utf-8")


def test_inventory_manifest_code_graph_and_surfaces(tmp_path: Path):
    _fixture_repo(tmp_path)
    inventory = build_repo_inventory(tmp_path)
    assert any(item["path"].endswith("runtime.py") for item in inventory["payload"]["files"])
    manifest = write_repo_inventory_manifest(tmp_path)
    assert verify_repo_inventory_manifest(Path(manifest["path"]).parent / "inventory-manifest.json")["status"] == "ok"
    graph = build_code_graph(tmp_path)
    assert "runtime.py" in graph["payload"]["nodes"]
    cli = build_cli_surface_map(tmp_path)
    assert cli["payload"]["count"] == 2
    dashboard = build_dashboard_surface_map(tmp_path)
    assert "Overview" in dashboard["payload"]["panels"]


def test_impact_test_selection_ownership_and_safety():
    changed = ["src/binance_spot_bot/runtime.py", "src/binance_spot_bot/security.py"]
    impact = impact_analysis(changed)
    assert impact["risk"]["payload"]["level"] == "critical"
    tests = select_tests_for_changes(changed)
    assert "tests/test_risk_execution_security.py" in tests["payload"]["tests"]
    ownership = build_code_ownership(changed)
    assert {item["owner"] for item in ownership["payload"]["files"]} >= {"runtime", "security_redaction"}
    surface = safety_surface_map(changed)
    assert surface["surfaces"]
    hints = repo_knowledge_codex_task_hints(changed)
    assert hints["live_trading_enabled"] is False


def test_traceability_artifacts_reports_store_and_refactors(tmp_path: Path):
    _fixture_repo(tmp_path)
    trace = build_roadmap_traceability(tmp_path)
    assert trace["edges"]
    artifacts = build_artifact_flow_graph(tmp_path)
    assert any(edge["source"] == "check-all" for edge in artifacts["edges"])
    report = build_repo_knowledge_report(tmp_path)
    paths = write_repo_knowledge_report(tmp_path, report)
    assert Path(paths["json"]).exists()
    store_paths = write_repo_knowledge_store(tmp_path, {"report": report, "artifact_flow": artifacts})
    assert verify_repo_knowledge_store(store_paths["manifest"])["status"] == "ok"
    refactors = detect_refactor_candidates(tmp_path, line_threshold=1)
    assert refactors["candidates"]


def test_docs_consistency_legacy_function():
    payload = docs_code_consistency(["docs/runtime.md"], ["runtime"])
    assert payload["status"] == "ok"
    assert payload["live_trading_enabled"] is False
