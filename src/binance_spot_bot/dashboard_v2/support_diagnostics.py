from __future__ import annotations

from pathlib import Path
from typing import Any

from .browser_smoke import dashboard_v2_browser_smoke_matrix
from .error_reports import recent_dashboard_v2_error_reports
from .performance_budgets import evaluate_dashboard_v2_performance_budgets
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .static_build import verify_dashboard_v2_static_build


def dashboard_v2_support_diagnostics(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    artifacts = {
        "static_build": verify_dashboard_v2_static_build(root),
        "performance_budget": evaluate_dashboard_v2_performance_budgets().to_dict(),
        "browser_smoke": dashboard_v2_browser_smoke_matrix(),
        "errors": recent_dashboard_v2_error_reports(root),
    }
    status = "blocked" if any(item.get("status") == "blocked" for item in artifacts.values()) else "ok"
    return redact_dashboard_payload(
        {
            "status": status,
            "artifacts": artifacts,
            "missing_optional_artifacts_are_warnings": True,
            "no_live_statement": dashboard_v2_no_live_statement(),
            "live_trading_enabled": False,
        }
    )
