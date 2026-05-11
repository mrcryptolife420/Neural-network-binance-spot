from __future__ import annotations

import hashlib
import json
import shutil
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from .redaction import redact_payload

SAFE_COMMANDS = {
    "diagnostics",
    "operator-report",
    "operator-quality-gate",
    "operator-health-score",
    "evidence-manifest",
    "report-index",
    "redaction-self-test",
    "local-ops-snapshot",
    "dashboard-smoke",
}
FORBIDDEN_SUFFIXES = {".env", ".pem", ".key"}


@dataclass(frozen=True)
class LocalRecord:
    record_id: str
    kind: str
    status: str = "ready"
    payload: dict[str, Any] = field(default_factory=dict)
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def safe_record(kind: str, payload: dict[str, Any] | None = None, *, status: str = "ready") -> dict[str, Any]:
    return LocalRecord(f"{kind}-{int(time.time() * 1000)}", kind, status, payload or {}).to_dict()


def is_safe_command(command: str) -> bool:
    parts = command.strip().split()
    return bool(parts) and parts[0] in SAFE_COMMANDS and not any(term in command.lower() for term in ["order", "withdraw", "live"])


def write_json_report(root: Path, area: str, name: str, payload: dict[str, Any]) -> dict[str, str]:
    out = root / area
    out.mkdir(parents=True, exist_ok=True)
    safe = redact_payload({**payload, "live_trading_enabled": False})
    json_path = out / f"{name}.json"
    md_path = out / f"{name}.md"
    json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md_path.write_text(f"# {name.replace('-', ' ').title()}\n\nStatus: {safe.get('status', 'ready')}\nLive trading: disabled\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def inventory(root: Path) -> dict[str, Any]:
    rows = []
    if root.exists():
        for path in sorted(p for p in root.rglob("*") if p.is_file())[:500]:
            forbidden = path.suffix.lower() in FORBIDDEN_SUFFIXES or path.name.lower() == ".env"
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                rows.append(
                    {
                        "path": str(path.relative_to(root)),
                        "suffix": path.suffix,
                        "size_bytes": path.stat().st_size,
                        "sha256": digest,
                        "include_eligible": not forbidden,
                        "restore_priority": "skip" if forbidden else "normal",
                    }
                )
            except OSError as exc:
                rows.append({"path": str(path), "error": str(exc), "include_eligible": False})
    return {"status": "ready", "items": rows, "live_trading_enabled": False}


def create_safe_zip(root: Path, output: Path) -> dict[str, Any]:
    inv = inventory(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for item in inv["items"]:
            if item.get("include_eligible"):
                source = root / item["path"]
                if source.exists():
                    archive.write(source, item["path"])
        archive.writestr("manifest.json", json.dumps(redact_payload(inv), indent=2))
    return {"status": "ok", "zip": str(output), "manifest": inv, "live_trading_enabled": False}


def verify_zip(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "blocked", "reason": "missing_backup", "live_trading_enabled": False}
    with ZipFile(path) as archive:
        names = archive.namelist()
        forbidden = [name for name in names if Path(name).suffix.lower() in FORBIDDEN_SUFFIXES or Path(name).name.lower() == ".env"]
    return {"status": "ok" if not forbidden else "blocked", "files": len(names), "forbidden": forbidden, "live_trading_enabled": False}


def restore_preview(zip_path: Path, target: Path) -> dict[str, Any]:
    verify = verify_zip(zip_path)
    creates = []
    conflicts = []
    if verify["status"] == "ok":
        with ZipFile(zip_path) as archive:
            for name in archive.namelist():
                destination = target / name
                (conflicts if destination.exists() else creates).append(name)
    return {"status": verify["status"], "creates": creates, "conflicts": conflicts, "preview_only": True, "live_trading_enabled": False}


def safe_answer(question: str) -> dict[str, Any]:
    lowered = question.lower()
    if any(term in lowered for term in ["place order", "withdraw", "live trading", "api secret"]):
        return {"status": "blocked", "answer": "Unsafe trading or secret request blocked.", "sources": [], "live_trading_enabled": False}
    return {"status": "answered", "answer": "Local paper/demo status can be reviewed through reports, metrics, and runbooks.", "sources": ["local_ops"], "live_trading_enabled": False}


def compliance_score(rows: list[dict[str, Any]]) -> dict[str, Any]:
    violations = [row for row in rows if row.get("allowed") is False and row.get("required") is True]
    score = max(0, 100 - len(violations) * 20)
    return {"status": "ok" if not violations else "warn", "score": score, "violations": violations, "live_trading_enabled": False}


def copy_bundle(files: list[Path], out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for file in files:
        if file.exists() and file.is_file():
            target = out / file.name
            shutil.copy2(file, target)
            rows.append({"file": target.name, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    manifest = {"status": "ok", "files": rows, "live_trading_enabled": False}
    (out / "manifest.json").write_text(json.dumps(redact_payload(manifest), indent=2), encoding="utf-8")
    return manifest
