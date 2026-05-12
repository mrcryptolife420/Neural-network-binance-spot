from __future__ import annotations

import ast
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TestCaseInfo:
    name: str
    kind: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TestFile:
    path: str
    sha256: str
    line_count: int
    test_count: int
    imported_source_modules: list[str]
    likely_domain: str
    safety_relevance: bool
    estimated_profile: str
    recommended_command: str
    tests: list[TestCaseInfo]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["tests"] = [test.to_dict() for test in self.tests]
        return payload


def _short_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:24]


def _domain(path: str) -> str:
    lower = path.lower()
    for domain in ["security", "redaction", "runtime", "operator", "dashboard", "ui", "roadmap", "release", "migration", "portfolio"]:
        if domain in lower:
            return "dashboard" if domain == "ui" else domain
    return "general"


def _profile(domain: str) -> str:
    if domain in {"security", "redaction", "runtime", "release", "migration"}:
        return "deep"
    if domain in {"dashboard", "operator", "roadmap"}:
        return "standard"
    return "fast"


def build_test_inventory(root: Path | str = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    files: list[TestFile] = []
    for path in sorted((root_path / "tests").rglob("test*.py")) if (root_path / "tests").exists() else []:
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        try:
            tree = ast.parse(text)
        except SyntaxError:
            tree = ast.Module(body=[], type_ignores=[])
        tests: list[TestCaseInfo] = []
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name.lower().startswith("test"):
                tests.append(TestCaseInfo(node.name, "unittest_class"))
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                tests.append(TestCaseInfo(node.name, "pytest_function"))
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("binance_spot_bot"):
                imports.append(node.module)
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names if alias.name.startswith("binance_spot_bot"))
        rel = path.relative_to(root_path).as_posix()
        domain = _domain(rel + " " + " ".join(imports))
        files.append(
            TestFile(
                path=rel,
                sha256=_short_hash(path),
                line_count=text.count("\n") + (1 if text else 0),
                test_count=len(tests),
                imported_source_modules=sorted(dict.fromkeys(imports)),
                likely_domain=domain,
                safety_relevance=domain in {"security", "redaction", "runtime", "release", "migration"},
                estimated_profile=_profile(domain),
                recommended_command=f"python -m pytest {rel} -q",
                tests=tests,
            )
        )
    return {"status": "ready", "payload": {"tests": [item.to_dict() for item in files], "count": len(files)}, "live_trading_enabled": False}


def write_test_inventory_manifest(root: Path | str = ".", out: Path | str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    payload = build_test_inventory(root_path)
    out_dir = Path(out) if out else root_path / "data" / "test-runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "test-inventory.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    manifest = {"status": "ready", "path": str(path), "sha256": _short_hash(path), "live_trading_enabled": False}
    manifest_path = out_dir / "test-inventory-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def verify_test_inventory_manifest(manifest_path: Path | str) -> dict[str, Any]:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    path = Path(manifest["path"])
    ok = path.exists() and _short_hash(path) == manifest["sha256"]
    return {"status": "ok" if ok else "failed", "live_trading_enabled": False}


def test_inventory(root: Path) -> dict[str, Any]:
    return build_test_inventory(root)
