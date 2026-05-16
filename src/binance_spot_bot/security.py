from __future__ import annotations

import re
from pathlib import Path

from .redaction import SECRET_PATTERNS


SECRET_REGEXES = [
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{24,}"),
    re.compile(r"(?i)binance(.{0,20})?(secret|api[_-]?key).{0,10}[:=]\s*['\"][A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(signature|listenKey)\s*[:=]\s*['\"]?[A-Za-z0-9_-]{16,}"),
    *SECRET_PATTERNS,
]


def scan_for_secrets(root: Path) -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    ignored_parts = {
        ".git",
        ".lean-ctx",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".streamlit",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "env",
        "node_modules",
        "venv",
    }
    for path in root.rglob("*"):
        relative_parts = path.relative_to(root).parts
        if (
            not path.is_file()
            or any(part in ignored_parts for part in relative_parts)
            or relative_parts[:2] == ("data", "pytest-tmp")
            or relative_parts[:2] == (".tmp", "check-all-temp")
            or path.name in {"package-lock.json", "npm-shrinkwrap.json"}
        ):
            continue
        if path.suffix.lower() not in {"", ".py", ".md", ".toml", ".txt", ".example", ".json", ".ps1", ".cmd"}:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines, start=1):
            for pattern in SECRET_REGEXES:
                if pattern.search(line):
                    findings.append((path, index, "possible secret"))
                    break
    return findings
