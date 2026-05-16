import json
import tempfile
from pathlib import Path

from binance_spot_bot.dashboard_v2.app import DashboardV2FallbackApp, create_dashboard_v2_app
from binance_spot_bot.dashboard_v2.widget_registry import widget_registry_payload
from binance_spot_bot.strategy_lab import PAPER_ONLY_CONFIRM, strategy_lab_health
from binance_spot_bot.strategy_lab.candidate_scorecards import build_candidate_scorecards
from binance_spot_bot.strategy_lab.experiment_evidence_bundle import export_strategy_lab_evidence
from binance_spot_bot.strategy_lab.experiment_matrix import expand_experiment_matrix
from binance_spot_bot.strategy_lab.experiment_queue import build_queue_from_candidates, validate_queue
from binance_spot_bot.strategy_lab.experiment_queue_store import StrategyExperimentQueueStore
from binance_spot_bot.strategy_lab.experiment_result_store import ExperimentResultStore
from binance_spot_bot.strategy_lab.paper_experiment_runner import run_paper_experiment_queue
from binance_spot_bot.strategy_lab.portfolio_candidate_research import build_portfolio_candidate_research
from binance_spot_bot.strategy_lab.research_guards import evaluate_research_guards
from binance_spot_bot.strategy_lab.scanner_candidate_builder import build_scanner_candidates
from binance_spot_bot.strategy_lab.strategy_comparison import compare_strategy_results


def test_scanner_candidates_queue_matrix_and_store_are_paper_only():
    candidates = build_scanner_candidates()
    assert candidates["status"] == "ok"
    assert candidates["candidates"]
    assert candidates["live_trading_enabled"] is False
    assert "financial advice" in candidates["no_advice_statement"].lower()

    queue = build_queue_from_candidates(list(candidates["candidates"]))
    assert queue["validation"]["status"] == "ok"
    assert queue["manifest"]["payload_hash"]
    assert queue["live_trading_enabled"] is False

    duplicate = dict(queue)
    duplicate["jobs"] = [queue["jobs"][0], queue["jobs"][0]]
    assert validate_queue_payload(duplicate)["status"] == "blocked"

    matrix = expand_experiment_matrix(list(candidates["candidates"]), preset="small_safe_smoke")
    assert matrix["status"] == "ok"
    assert matrix["expanded_jobs"] <= 2

    with tempfile.TemporaryDirectory() as tmp:
        store = StrategyExperimentQueueStore(Path(tmp) / "queues")
        saved = store.save(queue)
        assert saved["status"] == "ok"
        loaded = store.load(queue["queue_id"])
        assert loaded["queue_id"] == queue["queue_id"]
        assert store.export_manifest(queue["queue_id"])["status"] == "ok"


def validate_queue_payload(payload):
    from binance_spot_bot.strategy_lab.experiment_queue import StrategyExperimentJob, StrategyExperimentQueue

    jobs = tuple(StrategyExperimentJob(**job) for job in payload["jobs"])
    return validate_queue(StrategyExperimentQueue(payload["queue_id"], payload["name"], jobs))


def test_runner_results_comparison_scorecards_portfolio_guards_and_evidence_are_secret_free():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        candidates = build_scanner_candidates()
        queue = build_queue_from_candidates(list(candidates["candidates"]))
        assert run_paper_experiment_queue(queue, confirm="")["status"] == "blocked"
        report = run_paper_experiment_queue(queue, confirm=PAPER_ONLY_CONFIRM)
        assert report["status"] == "ok"
        assert all(row["live_trading_enabled"] is False for row in report["results"])

        store = ExperimentResultStore(root / "results")
        for row in report["results"]:
            store.save_job_result(row)
        results = store.list_results()["results"]
        assert results
        assert store.export(results)["status"] == "ok"

        comparison = compare_strategy_results(results)
        assert comparison["status"] == "ok"
        scorecards = build_candidate_scorecards(results, list(candidates["candidates"]))
        assert scorecards["status"] == "ok"
        portfolio = build_portfolio_candidate_research(list(scorecards["scorecards"]))
        assert portfolio["status"] == "ok"
        guards = evaluate_research_guards(results)
        assert guards["status"] == "ok"
        evidence = export_strategy_lab_evidence(root, {"comparison": comparison, "scorecards": scorecards, "portfolio": portfolio, "guards": guards})
        manifest = Path(evidence["manifest"]).read_text(encoding="utf-8")
        assert "STRATEGY LAB - PAPER ONLY - NO LIVE TRADING" in manifest
        assert "api_key" not in manifest.lower()
        json.loads(manifest)


def test_strategy_lab_dashboard_api_cli_surface_is_no_live():
    assert strategy_lab_health()["requires_api_keys"] is False
    widgets = widget_registry_payload()
    widget_types = {item["widget_type"] for item in widgets["widgets"]}
    assert {"scanner_candidate_table", "experiment_queue", "strategy_comparison", "candidate_scorecard", "experiment_evidence"} <= widget_types

    fallback = DashboardV2FallbackApp()
    assert fallback.strategy_lab_health()["live_trading_enabled"] is False

    app = create_dashboard_v2_app()
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return
    if isinstance(app, DashboardV2FallbackApp):
        return
    client = TestClient(app)
    assert client.get("/api/strategy-lab/health").json()["paper_only"] is True
    candidates = client.post("/api/strategy-lab/candidates/build").json()
    assert candidates["status"] == "ok"
    assert client.post("/api/strategy-lab/queue/preview").json()["status"] == "ok"
    saved = client.post("/api/strategy-lab/queue/create").json()
    queue_id = saved["queue"]["queue_id"]
    assert client.post(f"/api/strategy-lab/queues/{queue_id}/run").json()["status"] == "blocked"
    assert client.post(f"/api/strategy-lab/queues/{queue_id}/run?confirm={PAPER_ONLY_CONFIRM}").json()["status"] == "ok"
    assert client.get("/api/strategy-lab/results").json()["status"] == "ok"
    assert client.post("/api/strategy-lab/comparison").json()["status"] == "ok"
    assert client.post("/api/strategy-lab/scorecards").json()["status"] == "ok"
    assert client.post("/api/strategy-lab/evidence-export").json()["status"] == "ok"
