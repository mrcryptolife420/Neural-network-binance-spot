from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .redaction import redact_payload

FORBIDDEN_LIVE_PHRASES = ("live approved", "real funds", "production live", "place real order")


@dataclass(frozen=True)
class OperatorDocPage:
    doc_id: str
    title: str
    path: str
    category: str
    target_operator_level: str = "normal"
    related_cli_commands: list[str] | None = None
    related_dashboard_pages: list[str] | None = None
    related_playbooks: list[str] | None = None
    no_live_statement_present: bool = False
    missing_or_empty: bool = False
    forbidden_live_phrase_present: bool = False
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class OperatorDocSection:
    name: str
    pages: list[OperatorDocPage]


@dataclass(frozen=True)
class OperatorDocsIndex:
    status: str
    sections: list[OperatorDocSection]
    no_live_statement: str = "Operator docs are local-only and never approve live trading."
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class OperatorDocsValidationResult:
    status: str
    warnings: list[str]
    blockers: list[str]
    live_trading_enabled: bool = False


def _category(path: Path) -> str:
    parts = path.parts
    if "dashboard-walkthroughs" in parts:
        return "dashboard_walkthrough"
    if "cli-cookbook" in parts:
        return "cli_cookbook"
    if "troubleshooting" in parts:
        return "troubleshooting"
    if "support-bundles" in parts:
        return "support_bundle"
    if "evidence" in parts:
        return "evidence"
    return "operator_manual"


def build_operator_docs_index(root: Path | str = ".") -> OperatorDocsIndex:
    root = Path(root)
    docs_root = root / "docs" / "operator"
    pages: list[OperatorDocPage] = []
    if docs_root.exists():
        for path in sorted(docs_root.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            title = next((line.strip("# ").strip() for line in text.splitlines() if line.startswith("#")), path.stem.replace("-", " ").title())
            lowered = text.lower()
            pages.append(
                OperatorDocPage(
                    doc_id=path.stem,
                    title=title,
                    path=str(path.relative_to(root)),
                    category=_category(path),
                    related_cli_commands=[part.strip("`") for part in text.split() if part.startswith("`python")],
                    related_dashboard_pages=[],
                    related_playbooks=[],
                    no_live_statement_present="no live" in lowered or "live trading: disabled" in lowered,
                    missing_or_empty=not text.strip(),
                    forbidden_live_phrase_present=any(phrase in lowered for phrase in FORBIDDEN_LIVE_PHRASES),
                )
            )
    sections = [OperatorDocSection("operator", pages)]
    status = validate_operator_docs_index(OperatorDocsIndex("ok", sections)).status
    return OperatorDocsIndex(status, sections)


def validate_operator_docs_index(index: OperatorDocsIndex) -> OperatorDocsValidationResult:
    warnings: list[str] = []
    blockers: list[str] = []
    pages = [page for section in index.sections for page in section.pages]
    if not any(page.path.replace("\\", "/").endswith("docs/operator/index.md") for page in pages):
        blockers.append("missing docs/operator/index.md")
    for page in pages:
        if page.missing_or_empty:
            warnings.append(f"empty doc: {page.path}")
        if not page.no_live_statement_present:
            warnings.append(f"missing no-live statement: {page.path}")
        if page.forbidden_live_phrase_present:
            blockers.append(f"forbidden live approval phrase: {page.path}")
    return OperatorDocsValidationResult("blocked" if blockers else "warn" if warnings else "ok", warnings, blockers)


def operator_docs_index_to_dict(index: OperatorDocsIndex) -> dict[str, Any]:
    return redact_payload(asdict(index))


def operator_docs_index() -> dict[str, Any]:
    return operator_docs_index_to_dict(build_operator_docs_index(Path.cwd()))


def write_operator_docs_index(root: Path | str = ".") -> dict[str, str]:
    root = Path(root)
    index = build_operator_docs_index(root)
    payload = operator_docs_index_to_dict(index) | {"validated_at_ms": int(time.time() * 1000)}
    out = root / "data" / "operator-training" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "operator_docs_index.json"
    md_path = out / "operator_docs_index.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(f"# Operator Docs Index\n\nStatus: {payload['status']}\nLive trading: disabled\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}
