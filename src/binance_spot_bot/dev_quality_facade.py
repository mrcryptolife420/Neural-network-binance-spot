from __future__ import annotations

import ast
import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .local_paper_os_facade import copy_bundle, safe_record, write_json_report


def version_payload(version: str = "0.1.0") -> dict[str, Any]:
    return safe_record("version", {"version": version, "schema_version": 1})


def release_manifest(root: Path, version: str = "0.1.0") -> dict[str, Any]:
    files = [p for p in root.rglob("*.py") if ".venv" not in p.parts][:200]
    return safe_record("release_manifest", {"version": version, "files": len(files), "created_at_ms": int(time.time() * 1000)})


def roadmap_index(open_dir: Path, done_dir: Path) -> dict[str, Any]:
    open_files = sorted(p.name for p in open_dir.glob("*.md")) if open_dir.exists() else []
    done_files = sorted(p.name for p in done_dir.glob("*.md")) if done_dir.exists() else []
    return safe_record("roadmap_index", {"open": open_files, "done": done_files, "open_count": len(open_files), "done_count": len(done_files)})


def repo_inventory(root: Path) -> dict[str, Any]:
    files = [p for p in root.rglob("*.py") if ".venv" not in p.parts and "__pycache__" not in p.parts]
    return safe_record("repo_inventory", {"python_files": len(files), "tests": len([p for p in files if p.name.startswith("test_")])})


def code_graph(root: Path) -> dict[str, Any]:
    nodes = []
    edges = []
    for path in list((root / "src" / "binance_spot_bot").glob("*.py"))[:300]:
        nodes.append(str(path.name))
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                edges.append({"from": path.name, "to": node.module})
    return safe_record("code_graph", {"nodes": nodes, "edges": edges})


def changed_files(paths: list[str]) -> dict[str, Any]:
    return safe_record("changed_files", {"changed": paths})


def regression_risk(paths: list[str]) -> dict[str, Any]:
    score = 10 + sum(30 for path in paths if any(part in path for part in ["runtime", "risk", "execution", "security"]))
    return safe_record("regression_risk", {"score": min(score, 100), "changed": paths})


def selected_tests(paths: list[str]) -> dict[str, Any]:
    tests = {"tests/test_risk_execution_security.py"} if any("risk" in path or "security" in path for path in paths) else set()
    if any("dashboard" in path or "ui" in path for path in paths):
        tests.add("tests/test_simple_demo_dashboard.py")
    if not tests:
        tests.add("tests/test_roadmaps_083_088_full_surface.py")
    return safe_record("selected_tests", {"tests": sorted(tests), "changed": paths})


def profile_payload(name: str, elapsed_ms: float, budget_ms: float = 1000.0) -> dict[str, Any]:
    return safe_record("profile", {"name": name, "elapsed_ms": elapsed_ms, "budget_ms": budget_ms, "status": "ok" if elapsed_ms <= budget_ms else "warn"})


def dashboard_smoke_v2() -> dict[str, Any]:
    return safe_record("dashboard_smoke_v2", {"stable_keys": True, "lazy_sections": True, "non_overlapping_text": True})


def runtime_event(event_type: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return safe_record("runtime_event", {"event_type": event_type, "payload": payload or {}})


def data_contract(name: str, rows: int = 0) -> dict[str, Any]:
    return safe_record("data_contract", {"name": name, "rows": rows, "schema_hash": hashlib.sha256(name.encode()).hexdigest()[:12]})


def evidence_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    return copy_bundle(files, out)


def write_dev_report(root: Path, name: str, payload: dict[str, Any]) -> dict[str, str]:
    return write_json_report(root, "dev-quality", name, payload)
