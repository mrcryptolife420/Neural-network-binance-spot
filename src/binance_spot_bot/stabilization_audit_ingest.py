from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class StabilizationFindingSource:
    name: str
    path: str
    exists: bool


@dataclass(frozen=True)
class StabilizationFinding:
    finding_id: str
    source: StabilizationFindingSource
    category: str
    severity: str
    title: str
    description: str
    evidence_path: str = ""
    command: str = ""
    subsystem: str = "paper_os"
    roadmap: str = "101"
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class StabilizationIngestReport:
    status: str
    findings: list[StabilizationFinding]
    sources: list[StabilizationFindingSource]
    no_live_statement: str = "Paper OS stabilization is local, paper-only, and never enables live trading."
    live_trading_enabled: bool = False


ROADMAP100_ARTIFACTS = {
    "system_audit": "data/milestone/reports/system_audit_report.json",
    "production_readiness": "data/milestone/readiness/production_readiness_simulation.json",
    "safety_invariants": "data/milestone/safety-invariants/system_safety_invariants.json",
    "no_live_proof": "data/milestone/no-live/no_live_proof_pack.json",
    "paper_simulation": "data/milestone/paper-os-simulation/paper_os_simulation.json",
    "roadmap_traceability": "data/milestone/roadmap-traceability/roadmap_traceability_001_100.json",
}


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _finding(source: StabilizationFindingSource, category: str, severity: str, title: str, description: str) -> StabilizationFinding:
    return StabilizationFinding(
        finding_id=f"{category}-{abs(hash((source.name, title))) % 1_000_000:06d}",
        source=source,
        category=category,
        severity=severity,
        title=title,
        description=description,
        evidence_path=source.path,
    )


def ingest_roadmap100_reports(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    findings: list[StabilizationFinding] = []
    sources: list[StabilizationFindingSource] = []
    for name, relative in ROADMAP100_ARTIFACTS.items():
        path = root / relative
        source = StabilizationFindingSource(name=name, path=relative, exists=path.exists())
        sources.append(source)
        payload = _load_json(path) if path.exists() else None
        if payload is None:
            severity = "P0" if name == "no_live_proof" else "P1"
            findings.append(_finding(source, "missing_evidence", severity, f"Missing {name}", f"Expected Roadmap 100 artifact is missing: {relative}"))
            continue
        status = payload.get("status") or payload.get("payload", {}).get("status")
        if status in {"blocked", "failed", "fail"}:
            severity = "P0" if name in {"no_live_proof", "safety_invariants"} else "P1"
            findings.append(_finding(source, "failed_artifact", severity, f"{name} is {status}", "Roadmap 100 artifact reports a blocking status."))
        if payload.get("live_trading_enabled") is True:
            findings.append(_finding(source, "safety_no_live", "P0", f"{name} enables live trading", "Live trading must remain disabled."))
    status = "blocked" if any(finding.severity == "P0" for finding in findings) else "review" if findings else "ok"
    report = StabilizationIngestReport(status=status, findings=findings, sources=sources)
    return stabilization_ingest_report_to_dict(report)


def ingest_roadmap100_bundle(path: Path | str) -> dict[str, Any]:
    path = Path(path)
    manifest = path / "milestone_bundle_manifest.json"
    source = StabilizationFindingSource("milestone_bundle", str(manifest), manifest.exists())
    findings: list[StabilizationFinding] = []
    if not manifest.exists():
        findings.append(_finding(source, "missing_evidence", "P1", "Missing milestone bundle manifest", "Bundle manifest is required for stabilization ingest."))
    else:
        payload = _load_json(manifest) or {}
        if not any("no_live_proof" in row.get("path", "") for row in payload.get("files", [])):
            findings.append(_finding(source, "missing_evidence", "P0", "Missing no-live proof in bundle", "No-live proof must be included in the Roadmap 100 bundle."))
    report = StabilizationIngestReport(status="blocked" if findings else "ok", findings=findings, sources=[source])
    return stabilization_ingest_report_to_dict(report)


def stabilization_ingest_report_to_dict(report: StabilizationIngestReport) -> dict[str, Any]:
    return redact_payload(asdict(report))


def stabilization_audit_ingest(blockers: list[str]) -> dict[str, Any]:
    findings = [
        StabilizationFinding(
            finding_id=f"manual-{index}",
            source=StabilizationFindingSource("manual", "inline", True),
            category="manual_blocker",
            severity="P1",
            title=blocker,
            description="Manual blocker input.",
        )
        for index, blocker in enumerate(blockers)
    ]
    return stabilization_ingest_report_to_dict(StabilizationIngestReport("blocked" if findings else "ok", findings, []))


def write_stabilization_ingest_report(root: Path | str = ".", payload: dict[str, Any] | None = None) -> dict[str, str]:
    root = Path(root)
    payload = payload or ingest_roadmap100_reports(root)
    out = root / "data" / "stabilization" / "ingest"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "stabilization_ingest_report.json"
    md_path = out / "stabilization_ingest_report.md"
    safe = redact_payload(payload | {"created_at_ms": int(time.time() * 1000)})
    json_path.write_text(json.dumps(safe, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        f"# Stabilization Ingest Report\n\nStatus: {safe['status']}\nFindings: {len(safe['findings'])}\nLive trading: disabled\n",
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}
