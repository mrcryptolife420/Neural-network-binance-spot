from __future__ import annotations


def classify_codex_task(issue_id: str) -> dict[str, object]:
    mapping = {"streamlit_duplicate_element_id": "dashboard_fix", "module_not_found": "dependency_fix", "secret_leak": "safety_blocker"}
    task = mapping.get(issue_id, "unknown_investigate_first")
    return {"status": "ok", "task_class": task, "forbidden_files": ["live execution adapters"] if task == "safety_blocker" else [], "required_tests": ["pytest -q"], "live_trading_enabled": False}

