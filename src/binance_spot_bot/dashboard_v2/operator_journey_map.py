from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload


@dataclass(frozen=True)
class OperatorJourneyStep:
    key: str
    label: str
    route: str
    fallback_route: str
    no_live_step: bool = False


@dataclass(frozen=True)
class OperatorJourney:
    key: str
    title: str
    primary_route: str
    fallback_route: str
    steps: list[OperatorJourneyStep]


def dashboard_v2_operator_journey_map() -> dict[str, Any]:
    journeys = [
        OperatorJourney(
            "beginner",
            "Beginner",
            "/",
            "/streamlit-legacy",
            [
                OperatorJourneyStep("open", "Open dashboard", "/", "/streamlit-legacy"),
                OperatorJourneyStep("no_live", "Verify no-live", "/", "/streamlit-legacy", True),
                OperatorJourneyStep("demo", "Run demo smoke", "/start", "/streamlit-legacy"),
                OperatorJourneyStep("evidence", "Export evidence", "/evidence", "/streamlit-legacy"),
            ],
        ),
        OperatorJourney(
            "paper_operator",
            "Paper Operator",
            "/paper-session-workflow",
            "/streamlit-legacy",
            [
                OperatorJourneyStep("no_live", "Verify no-live", "/", "/streamlit-legacy", True),
                OperatorJourneyStep("configure", "Configure symbol and risk", "/start", "/streamlit-legacy"),
                OperatorJourneyStep("monitor", "Monitor session", "/paper-session-workflow", "/streamlit-legacy"),
                OperatorJourneyStep("review", "Review report", "/sessions", "/streamlit-legacy"),
            ],
        ),
        OperatorJourney(
            "demo_spot_operator",
            "Demo Spot Operator",
            "/demo-spot-guided",
            "/streamlit-legacy",
            [
                OperatorJourneyStep("no_live", "Verify demo only", "/", "/streamlit-legacy", True),
                OperatorJourneyStep("profile", "Check demo profile", "/demo-spot-guided", "/streamlit-legacy"),
                OperatorJourneyStep("preview", "Preview demo order", "/demo-spot-guided", "/streamlit-legacy"),
                OperatorJourneyStep("reconcile", "Reconcile demo order", "/orders-account", "/streamlit-legacy"),
            ],
        ),
    ]
    return redact_dashboard_payload(
        {
            "status": "ok",
            "journeys": [asdict(item) for item in journeys],
            "missing_pages": [],
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )


def write_dashboard_v2_operator_journey_map(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    payload = dashboard_v2_operator_journey_map()
    out = root / "data" / "dashboard-v2" / "ux"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "operator-journey-map.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return {"status": "ok", "path": str(path), "report": payload, "live_trading_enabled": False}
