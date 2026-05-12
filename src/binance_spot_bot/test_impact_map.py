from __future__ import annotations

from typing import Any


def select_tests_for_changes(changed: list[str], strict: bool = False) -> dict[str, Any]:
    tests: list[str] = []
    reasons: list[dict[str, str]] = []
    def add(test: str, reason: str) -> None:
        if test not in tests:
            tests.append(test)
            reasons.append({"test": test, "reason": reason})
    for path in changed:
        lower = path.lower()
        if "/ui/" in lower or "streamlit_app.py" in lower:
            add("python -m binance_spot_bot.cli dashboard-smoke --seconds 1", "dashboard changed")
            add("python -m binance_spot_bot.cli dashboard-browser-smoke --url http://127.0.0.1:8506/ --seconds 10", "dashboard changed")
        if "cli.py" in lower:
            add("python -m binance_spot_bot.cli check-all --skip-tests --json", "cli surface changed")
        if any(token in lower for token in ["security", "redaction", "credentials"]):
            add("tests/test_risk_execution_security.py", "security surface changed")
            add("python -m binance_spot_bot.cli redaction-self-test --json", "redaction changed")
        if any(token in lower for token in ["runtime", "execution", "risk"]):
            add("tests/test_runtime_pilot_runner.py", "runtime/execution risk changed")
        if any(token in lower for token in ["evaluation", "features", "dataset"]):
            add("tests/test_evaluation.py", "model/evaluation data changed")
        if "roadmap docs" in lower or "roadmap_" in lower:
            add("tests/test_roadmap_090_roadmap_execution_acceptance.py", "roadmap execution changed")
        if any(token in lower for token in ["release", "migration"]):
            add("tests/test_roadmap_089_release_management_acceptance.py", "release/migration changed")
    if strict:
        add("python -m pytest -q", "strict profile")
    return {"status": "ready", "payload": {"tests": tests, "reasons": reasons, "strict": strict}, "live_trading_enabled": False}


def test_impact_map(changed: list[str]) -> dict[str, Any]:
    return select_tests_for_changes(changed)
