from __future__ import annotations

import ast
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class RepoFile:
    path: str
    suffix: str
    size_bytes: int
    modified_at: float
    sha256: str
    category: str
    line_count: int
    class_count: int
    function_count: int
    import_count: int
    has_tests_guess: bool
    safety_relevant_guess: bool
    secret_scan_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoDirectorySummary:
    directory: str
    file_count: int
    size_bytes: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoInventory:
    files: list[RepoFile]
    directories: list[RepoDirectorySummary]

    def to_dict(self) -> dict[str, Any]:
        return {"files": [item.to_dict() for item in self.files], "directories": [item.to_dict() for item in self.directories]}


def _short_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:24]


def _category(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel.startswith("src/"):
        return "source"
    if rel.startswith("tests/"):
        return "test"
    if rel.startswith("Roadmap docs/"):
        return "roadmap"
    if rel.startswith("Voltooid docs/"):
        return "completed_roadmap"
    if rel.startswith("docs/"):
        return "docs"
    if rel.startswith("scripts/"):
        return "script"
    if path.name in {"pyproject.toml", "README.md", ".gitignore"}:
        return "config"
    if rel.startswith("data/"):
        return "artifact"
    return "unknown"


def _python_counts(text: str) -> tuple[int, int, int]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return 0, 0, 0
    classes = sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
    functions = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))
    imports = sum(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))
    return classes, functions, imports


def _safety_guess(rel: str) -> bool:
    return any(token in rel.lower() for token in ["risk", "execution", "security", "redaction", "credentials", "live", "order", "permission", "backup", "restore", "migration"])


def _secret_scan_text(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ["api_secret", "secret key:", "private_key", "-----begin"]):
        return "redacted"
    return "ok"


def build_repo_inventory_object(root: Path | str = ".") -> RepoInventory:
    root_path = Path(root).resolve()
    include_roots = [root_path / name for name in ["src", "tests", "docs", "Roadmap docs", "Voltooid docs", "scripts"]]
    root_files = [root_path / name for name in ["pyproject.toml", "README.md", ".gitignore"]]
    files: list[RepoFile] = []
    candidates: list[Path] = []
    for directory in include_roots:
        if directory.exists():
            candidates.extend(path for path in directory.rglob("*") if path.is_file())
    candidates.extend(path for path in root_files if path.exists())
    for path in sorted(set(candidates)):
        try:
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
        except OSError:
            text = ""
        classes, functions, imports = _python_counts(text) if path.suffix == ".py" else (0, 0, 0)
        rel = path.relative_to(root_path).as_posix()
        files.append(
            RepoFile(
                path=rel,
                suffix=path.suffix,
                size_bytes=path.stat().st_size,
                modified_at=path.stat().st_mtime,
                sha256=_short_hash(path),
                category=_category(path, root_path),
                line_count=text.count("\n") + (1 if text else 0),
                class_count=classes,
                function_count=functions,
                import_count=imports,
                has_tests_guess=(root_path / "tests" / f"test_{path.stem}.py").exists(),
                safety_relevant_guess=_safety_guess(rel),
                secret_scan_status=_secret_scan_text(text),
            )
        )
    by_dir: dict[str, list[RepoFile]] = {}
    for file in files:
        by_dir.setdefault(str(Path(file.path).parent).replace("\\", "/"), []).append(file)
    dirs = [RepoDirectorySummary(directory=key, file_count=len(value), size_bytes=sum(item.size_bytes for item in value)) for key, value in sorted(by_dir.items())]
    return RepoInventory(files, dirs)


def build_repo_inventory(root: Path | str = ".") -> dict[str, Any]:
    inventory = build_repo_inventory_object(root)
    return {"status": "ready", "payload": inventory.to_dict(), "live_trading_enabled": False}


def repo_inventory(root: Path | str = ".") -> dict[str, Any]:
    return build_repo_inventory(root)


def write_repo_inventory_manifest(root: Path | str = ".", out: Path | str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    payload = build_repo_inventory(root)
    out_dir = Path(out) if out else root_path / "data" / "repository-knowledge"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "inventory.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    manifest = {"status": "ready", "path": str(path), "sha256": _short_hash(path), "file_count": len(payload["payload"]["files"]), "live_trading_enabled": False}
    (out_dir / "inventory-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def verify_repo_inventory_manifest(manifest_path: Path | str) -> dict[str, Any]:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    path = Path(manifest["path"])
    ok = path.exists() and _short_hash(path) == manifest["sha256"]
    return {"status": "ok" if ok else "failed", "live_trading_enabled": False}
