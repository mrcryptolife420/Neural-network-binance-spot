from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .check_all import payload_for, run_checks
from .config import BotSettings
from .control_center import build_launch_plan
from .dashboard_browser_smoke import run_dashboard_browser_smoke
from .dashboard_evidence import build_operator_evidence, write_launch_evidence, write_operator_evidence
from .demo_execution_sandbox import DemoExecutionSandbox, intent_from_values
from .diagnostics import write_diagnostics_report
from .evidence_scorecard import generate_evidence_scorecard, write_scorecard
from .pilot_orchestrator import DemoPilotOrchestrator, PilotRunStore
from .preflight import run_preflight
from .redaction import redact_payload
from .ui.chart_registry import all_chart_keys
from .ui.page_registry import PAGES, validate_page_registry


@dataclass(frozen=True)
class RehearsalStep:
    name: str
    status: str
    message: str = ""
    artifact: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class RehearsalSummary:
    run_id: str
    status: str
    started_at_ms: int
    finished_at_ms: int
    duration_seconds: float
    steps: list[RehearsalStep]
    artifacts: dict[str, str]
    scorecard_status: str
    blockers: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)
    next_safe_action: str = ""
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                "run_id": self.run_id,
                "status": self.status,
                "started_at_ms": self.started_at_ms,
                "finished_at_ms": self.finished_at_ms,
                "duration_seconds": self.duration_seconds,
                "steps": [step.to_dict() for step in self.steps],
                "artifacts": self.artifacts,
                "scorecard_status": self.scorecard_status,
                "blockers": self.blockers,
                "warnings": self.warnings,
                "next_safe_action": self.next_safe_action,
                "live_trading_enabled": False,
            }
        )


class RehearsalHistory:
    def __init__(self, data_dir: Path) -> None:
        self.root = data_dir / "evidence" / "rehearsals"
        self.history_path = self.root / "history.jsonl"
        self.latest_path = self.root / "latest.json"

    def append(self, summary: RehearsalSummary) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        payload = summary.to_dict()
        with self.history_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, default=str) + "\n")
        self.latest_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    def latest(self) -> dict[str, Any]:
        if not self.latest_path.exists():
            return {}
        try:
            return json.loads(self.latest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def list_recent(self, limit: int = 20) -> list[dict[str, Any]]:
        if not self.history_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in self.history_path.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return rows[-limit:]

    def trend_points(self, limit: int = 50) -> list[dict[str, Any]]:
        points: list[dict[str, Any]] = []
        for row in self.list_recent(limit):
            points.append(
                {
                    "timestamp_ms": row.get("finished_at_ms", 0),
                    "status": row.get("status", "unknown"),
                    "scorecard_status": row.get("scorecard_status", "unknown"),
                    "blockers": len(row.get("blockers", [])),
                    "warnings": len(row.get("warnings", [])),
                    "duration_seconds": row.get("duration_seconds", 0),
                    "artifact_count": len(row.get("artifacts", {})),
                }
            )
        return points


class DemoAcceptanceRehearsal:
    def __init__(self, settings: BotSettings, project_root: Path) -> None:
        self.settings = settings
        self.project_root = project_root
        self.history = RehearsalHistory(settings.data_dir)

    def run(self, *, browser_url: str = "") -> RehearsalSummary:
        started = int(time.time() * 1000)
        run_id = f"rehearsal-{started}"
        run_dir = self.settings.data_dir / "evidence" / "rehearsals" / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        steps: list[RehearsalStep] = []
        artifacts: dict[str, str] = {}

        self._validate_config(steps)
        self._preflight(steps)
        self._launch_evidence(steps, artifacts)
        self._dashboard_smoke(steps, artifacts)
        self._browser_smoke(browser_url, steps, artifacts)
        self._check_all(steps, artifacts)
        self._pilot_idempotent_start_smoke(steps, artifacts)
        self._operator_diagnostics(steps, artifacts)
        self._demo_execution_preview(steps, artifacts)
        self._demo_execution_test_order(steps)
        self._operator_evidence(steps, artifacts)
        self._scorecard(steps, artifacts)

        scorecard_payload = self._load_json(Path(artifacts.get("scorecard", "")))
        scorecard_status = str(scorecard_payload.get("status", "warn"))
        blockers = scorecard_payload.get("blockers", [])
        warnings = scorecard_payload.get("warnings", [])
        status = "fail" if any(step.status == "failed" for step in steps) or scorecard_status == "fail" else "warn" if any(step.status in {"warn", "skipped"} for step in steps) or scorecard_status == "warn" else "pass"
        finished = int(time.time() * 1000)
        summary = RehearsalSummary(
            run_id=run_id,
            status=status,
            started_at_ms=started,
            finished_at_ms=finished,
            duration_seconds=round((finished - started) / 1000, 3),
            steps=steps,
            artifacts=artifacts,
            scorecard_status=scorecard_status,
            blockers=blockers,
            warnings=warnings,
            next_safe_action=str(scorecard_payload.get("next_safe_action", "Review rehearsal evidence.")),
        )
        summary_path = run_dir / "summary.json"
        artifacts_path = run_dir / "artifacts.json"
        summary_path.write_text(json.dumps(summary.to_dict(), indent=2, default=str), encoding="utf-8")
        artifacts_path.write_text(json.dumps(redact_payload(artifacts), indent=2, default=str), encoding="utf-8")
        artifacts["summary"] = str(summary_path)
        artifacts["artifacts"] = str(artifacts_path)
        final_summary = RehearsalSummary(
            run_id=run_id,
            status=status,
            started_at_ms=started,
            finished_at_ms=finished,
            duration_seconds=round((finished - started) / 1000, 3),
            steps=steps,
            artifacts=artifacts,
            scorecard_status=scorecard_status,
            blockers=blockers,
            warnings=warnings,
            next_safe_action=str(scorecard_payload.get("next_safe_action", "Review rehearsal evidence.")),
        )
        summary_path.write_text(json.dumps(final_summary.to_dict(), indent=2, default=str), encoding="utf-8")
        self.history.append(final_summary)
        return final_summary

    def _validate_config(self, steps: list[RehearsalStep]) -> None:
        try:
            self.settings.validate_startup()
            steps.append(RehearsalStep("validate-config", "ok", "configuration validates"))
        except Exception as exc:
            steps.append(RehearsalStep("validate-config", "failed", str(exc)))

    def _preflight(self, steps: list[RehearsalStep]) -> None:
        report = run_preflight(self.settings, self.project_root).to_dict()
        steps.append(RehearsalStep("preflight", "ok" if report.get("status") == "ok" else "failed", str(report.get("status"))))

    def _launch_evidence(self, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        plan = build_launch_plan(self.project_root)
        path = write_launch_evidence(self.settings.data_dir, plan.to_dict(), preflight_status="rehearsal")
        artifacts["launch_evidence"] = str(path)
        steps.append(RehearsalStep("launch-evidence", "ok", "launch plan evidence written", str(path)))

    def _dashboard_smoke(self, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        validate_page_registry()
        chart_keys = all_chart_keys()
        payload = {
            "status": "ok",
            "pages": [page.key for page in PAGES],
            "chart_keys": list(chart_keys),
            "unique_chart_keys": len(chart_keys) == len(set(chart_keys)),
            "live_trading_enabled": False,
        }
        path = self.settings.data_dir / "checks" / "dashboard-smoke.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        artifacts["dashboard_smoke"] = str(path)
        steps.append(RehearsalStep("dashboard-smoke", "ok", "static dashboard smoke ok", str(path)))

    def _browser_smoke(self, browser_url: str, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        if not browser_url:
            steps.append(RehearsalStep("dashboard-browser-smoke", "skipped", "browser URL not provided"))
            return
        payload = run_dashboard_browser_smoke(browser_url, self.settings.data_dir, seconds=15)
        artifacts["browser_smoke"] = str(payload.get("path", ""))
        steps.append(RehearsalStep("dashboard-browser-smoke", "ok" if payload.get("status") == "ok" else "failed", str(payload.get("status")), str(payload.get("path", ""))))

    def _check_all(self, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        payload = payload_for(run_checks(self.project_root, skip_tests=True))
        path = self.settings.data_dir / "checks" / "check-all.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        artifacts["check_all"] = str(path)
        steps.append(RehearsalStep("check-all", "ok" if payload.get("status") == "ok" else "failed", str(payload.get("status")), str(path)))

    def _pilot_idempotent_start_smoke(self, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        store = PilotRunStore(self.settings.data_dir / "evidence" / "pilot-idempotency-runs")
        orchestrator = DemoPilotOrchestrator(self.settings, store)
        payload = {
            "status": "created",
            "symbol": "BTCUSDT",
            "exchange_profile": {"name": "binance-demo-spot"},
            "credential_status": {"has_api_key": True, "has_api_secret": True, "capability": "rehearsal"},
            "demo_connection": {
                "profile": "binance-demo-spot",
                "base_url": "https://demo-api.binance.com",
                "armed": True,
                "connected": True,
                "authenticated": True,
                "gate": {"checks": {"filters_loaded": True, "demo_base_url": True}, "reason": "allowed"},
            },
            "demo_account": {"status": "ok", "can_trade": True},
            "demo_open_orders": [],
            "reconciliation": {"status": "ok", "orphan_orders": 0, "failures": 0, "needs_operator_action": False},
            "testnet_prechecks": {"risk_limits_set": True},
            "demo_pilot": {"config": {"pilot_name": "smoke"}, "counters": {}},
            "resume_required": False,
        }
        first = orchestrator.mark_running(payload)
        second = orchestrator.mark_running(payload)
        invalid_transition = any(item.get("from") == "running" and item.get("to") == "ready" for item in second.transitions)
        result = {
            "status": "ok" if first.run_id == second.run_id and second.state == "running" and not invalid_transition else "failed",
            "first_run_id": first.run_id,
            "second_run_id": second.run_id,
            "same_run_id": first.run_id == second.run_id,
            "state": second.state,
            "invalid_running_to_ready_transition": invalid_transition,
            "live_trading_enabled": False,
        }
        path = self.settings.data_dir / "evidence" / "pilot-start-idempotency.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(redact_payload(result), indent=2), encoding="utf-8")
        artifacts["pilot_start_idempotency"] = str(path)
        steps.append(RehearsalStep("pilot-idempotent-start-smoke", "ok" if result["status"] == "ok" else "failed", str(result["status"]), str(path)))

    def _demo_execution_preview(self, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        result = DemoExecutionSandbox(self.settings).preview(intent_from_values("BTCUSDT", "BUY", "10", "100"))
        artifacts["demo_execution"] = result.evidence_path
        steps.append(RehearsalStep("demo-execution-preview", "ok" if result.status == "PREVIEW_READY" else "failed", result.status, result.evidence_path))

    def _operator_diagnostics(self, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        path = write_diagnostics_report(self.settings, self.project_root)
        payload = self._load_json(path)
        status = str(payload.get("status", "warn"))
        artifacts["operator_diagnostics"] = str(path)
        steps.append(RehearsalStep("operator-diagnostics", "ok" if status == "ok" else "warn" if status == "warn" else "failed", status, str(path)))

    def _demo_execution_test_order(self, steps: list[RehearsalStep]) -> None:
        if not (self.settings.binance_api_key and self.settings.binance_api_secret):
            steps.append(RehearsalStep("demo-execution-test-order", "skipped", "Demo Spot credentials not configured"))
            return
        result = DemoExecutionSandbox(self.settings).test_order_only(intent_from_values("BTCUSDT", "BUY", "10", "100"))
        steps.append(RehearsalStep("demo-execution-test-order", "ok" if result.status == "TEST_ORDER_ACCEPTED" else "warn", result.status, result.evidence_path))

    def _operator_evidence(self, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        payload = build_operator_evidence(self.settings, mode="demo", profile=self.settings.exchange_profile, source="demo")
        path = write_operator_evidence(self.settings, payload)
        artifacts["operator_evidence"] = str(path)
        steps.append(RehearsalStep("dashboard-operator-evidence", "ok", "operator evidence written", str(path)))

    def _scorecard(self, steps: list[RehearsalStep], artifacts: dict[str, str]) -> None:
        scorecard = generate_evidence_scorecard(self.settings, write=False)
        path = write_scorecard(self.settings, scorecard)
        artifacts["scorecard"] = str(path)
        steps.append(RehearsalStep("evidence-scorecard", scorecard.status if scorecard.status in {"pass", "warn"} else "failed", scorecard.status, str(path)))

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
