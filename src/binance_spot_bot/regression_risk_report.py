from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .intelligent_test_selector import select_intelligent_tests


def build_regression_risk_report(changed: list[str]) -> dict[str, Any]:
    selection = select_intelligent_tests(changed)
    return {
        "status": "ready" if selection["status"] == "ready" else "blocked",
        "changed_files": changed,
        "risk": selection["risk"],
        "selected_profile": selection["selected_profile"],
        "required_tests": selection["selected_commands"],
        "blockers": selection["blockers"],
        "estimated_runtime_ms": selection["estimated_runtime_ms"],
        "no_live_proof": True,
        "live_trading_enabled": False,
    }


def write_regression_risk_report(root: Path, payload: dict) -> dict[str, str]:
    out = root / "data" / "test-runs" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "regression-risk-report.json"
    md_path = out / "regression-risk-report.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        "\n".join(
            [
                "# Regression Risk Report",
                "",
                f"- Risk: {payload['risk']['level']} ({payload['risk']['score']})",
                f"- Profile: {payload['selected_profile']}",
                f"- Required tests: {len(payload['required_tests'])}",
                "- Live trading enabled: false",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
