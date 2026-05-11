from __future__ import annotations

import html
import hashlib
import importlib.metadata
import json
import sys
import time
import zipfile
from pathlib import Path
from typing import Any

from .config import BotSettings
from .diagnostics import OperatorDiagnostics
from .redaction import redact_payload, redact_text
from .security import scan_for_secrets
from .support_bundle import create_support_bundle, verify_support_bundle


RETENTION_ROOTS = ("checks", "evidence", "sessions", "pilot-runs", "support")
CATALOG_ROOTS = ("checks", "evidence", "reports", "support", "sessions", "pilot-runs")


def artifact_catalog(
    settings: BotSettings,
    *,
    limit: int = 500,
    category: str = "",
    suffix: str = "",
    stale_days: int = 7,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    now = time.time()
    for root_name in CATALOG_ROOTS:
        if category and root_name != category:
            continue
        root = settings.data_dir / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            age_seconds = max(0, int(now - stat.st_mtime))
            file_suffix = path.suffix.lower()
            if suffix and file_suffix != suffix.lower():
                continue
            rows.append(
                {
                    "category": root_name,
                    "path": str(path),
                    "suffix": file_suffix,
                    "size_bytes": stat.st_size,
                    "age_seconds": age_seconds,
                    "stale": age_seconds > stale_days * 24 * 60 * 60,
                    "redacted": True,
                }
            )
    rows.sort(key=lambda item: str(item["path"]))
    summaries = _catalog_summaries(rows)
    return redact_payload({"status": "ok", "artifacts": rows[:limit], "count": len(rows), "summaries": summaries, "live_trading_enabled": False})


def operator_health_score(settings: BotSettings) -> dict[str, Any]:
    diagnostics = OperatorDiagnostics(settings).state_health().to_dict()
    blockers = diagnostics.get("blockers", [])
    warnings = diagnostics.get("warnings", [])
    score = max(0, 100 - len(blockers) * 30 - len(warnings) * 8)
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D"
    priorities: list[dict[str, str]] = []
    for item in blockers:
        priorities.append({"priority": "P0", "name": str(item.get("name", "blocker")), "action": str(item.get("next_action", "Resolve blocker"))})
    for item in warnings[:5]:
        priorities.append({"priority": "P1", "name": str(item.get("name", "warning")), "action": str(item.get("next_action", "Review warning"))})
    if not priorities:
        priorities.append({"priority": "P2", "name": "healthy", "action": "No operator action required"})
    return redact_payload(
        {
            "status": "ok" if not blockers else "fail",
            "score": score,
            "grade": grade,
            "severity_counts": {"blockers": len(blockers), "warnings": len(warnings)},
            "priorities": priorities,
            "next_best_action": priorities[0]["action"],
            "live_trading_enabled": False,
        }
    )


def rehearsal_profiles() -> dict[str, Any]:
    profiles = [
        {"name": "fast", "duration": "short", "use_case": "quick local sanity", "steps": ["validate-config", "preflight", "check-all", "operator-diagnostics"]},
        {"name": "standard", "duration": "medium", "use_case": "normal demo readiness", "steps": ["dashboard-smoke", "pilot-idempotent-start-smoke", "demo-execution-preview", "evidence-scorecard"]},
        {"name": "deep", "duration": "long", "use_case": "full operator acceptance", "steps": ["browser-smoke", "support-bundle", "operator-report", "security-scan"]},
    ]
    return {"status": "ok", "profiles": profiles, "live_trading_enabled": False}


def operator_report_diff(settings: BotSettings) -> dict[str, Any]:
    index = report_index(settings)
    reports = [Path(row["path"]) for row in index.get("reports", []) if str(row.get("suffix")) == ".md"]
    if not reports:
        return {"status": "empty", "reports": 0, "live_trading_enabled": False}
    if len(reports) == 1:
        return {"status": "single", "reports": 1, "latest": str(reports[0]), "live_trading_enabled": False}
    prev, latest = reports[-2], reports[-1]
    prev_text = prev.read_text(encoding="utf-8", errors="replace")
    latest_text = latest.read_text(encoding="utf-8", errors="replace")
    return redact_payload(
        {
            "status": "unchanged" if prev_text == latest_text else "changed",
            "previous": str(prev),
            "latest": str(latest),
            "size_delta": latest.stat().st_size - prev.stat().st_size,
            "updated_delta_seconds": int(latest.stat().st_mtime - prev.stat().st_mtime),
            "live_trading_enabled": False,
        }
    )


def support_bundle_restore_preview(bundle_zip: Path) -> dict[str, Any]:
    if not bundle_zip.exists():
        return {"status": "fail", "bundle": str(bundle_zip), "errors": ["bundle missing"], "live_trading_enabled": False}
    try:
        with zipfile.ZipFile(bundle_zip, "r") as archive:
            names = archive.namelist()
            if "manifest.json" not in names:
                return {"status": "fail", "bundle": str(bundle_zip), "errors": ["manifest missing"], "live_trading_enabled": False}
            manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        return {"status": "fail", "bundle": str(bundle_zip), "errors": [str(exc)], "live_trading_enabled": False}
    suffixes: dict[str, int] = {}
    for item in manifest.get("files", []):
        suffix = Path(str(item.get("path", ""))).suffix.lower() or "none"
        suffixes[suffix] = suffixes.get(suffix, 0) + 1
    return redact_payload(
        {
            "status": "ok",
            "bundle": str(bundle_zip),
            "files": len(manifest.get("files", [])),
            "suffixes": suffixes,
            "redacted": all(bool(item.get("redacted")) for item in manifest.get("files", [])),
            "mode": "preview-only",
            "live_trading_enabled": False,
        }
    )


def evidence_chain(settings: BotSettings) -> dict[str, Any]:
    catalog = artifact_catalog(settings, limit=1000).get("artifacts", [])
    previous = "0" * 64
    chain: list[dict[str, Any]] = []
    for item in catalog:
        path = Path(str(item.get("path", "")))
        if not path.is_file():
            continue
        content = redact_text(path.read_text(encoding="utf-8", errors="replace"))
        digest = hashlib.sha256((previous + content).encode("utf-8")).hexdigest()
        chain.append({"path": str(path), "sha256": _format_digest(digest), "previous": _format_digest(previous)})
        previous = digest
    out = settings.data_dir / "evidence" / "manifest" / "evidence-chain.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"status": "ok", "chain": chain, "count": len(chain), "live_trading_enabled": False}
    out.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return {"status": "ok", "path": str(out), "count": len(chain), "live_trading_enabled": False}


def environment_doctor(settings: BotSettings) -> dict[str, Any]:
    packages = {}
    for package in ("streamlit", "plotly", "pytest"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "missing"
    checks = [
        {"check": "python", "status": "ok", "detail": sys.version.split()[0]},
        {"check": "data_dir", "status": "ok" if _can_write(settings.data_dir) else "fail", "detail": str(settings.data_dir)},
        {"check": "audit_dir", "status": "ok" if _can_write(settings.audit_log_path.parent) else "fail", "detail": str(settings.audit_log_path.parent)},
        {"check": "project_root", "status": "ok", "detail": str(Path.cwd())},
    ]
    checks.extend({"check": f"package_{name}", "status": "ok" if version != "missing" else "warn", "detail": version} for name, version in packages.items())
    return redact_payload({"status": "fail" if any(row["status"] == "fail" for row in checks) else "ok", "checks": checks, "live_trading_enabled": False})


def data_growth_budget(settings: BotSettings, *, budget_bytes: int = 100_000_000) -> dict[str, Any]:
    catalog = artifact_catalog(settings, limit=10_000).get("artifacts", [])
    total = sum(int(row.get("size_bytes", 0)) for row in catalog)
    by_category: dict[str, int] = {}
    for row in catalog:
        by_category[str(row.get("category", "unknown"))] = by_category.get(str(row.get("category", "unknown")), 0) + int(row.get("size_bytes", 0))
    largest = sorted(catalog, key=lambda row: int(row.get("size_bytes", 0)), reverse=True)[:10]
    return redact_payload(
        {
            "status": "warn" if total > budget_bytes else "ok",
            "total_size_bytes": total,
            "budget_bytes": budget_bytes,
            "budget_used_pct": round((total / budget_bytes) * 100, 2) if budget_bytes else 0,
            "by_category": by_category,
            "largest_files": largest,
            "live_trading_enabled": False,
        }
    )


def diagnostics_baseline(settings: BotSettings, *, write: bool = False) -> dict[str, Any]:
    path = settings.data_dir / "evidence" / "diagnostics" / "baseline.json"
    current = OperatorDiagnostics(settings).state_health().to_dict()
    if write or not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(current, indent=2, default=str), encoding="utf-8")
        baseline = current
        mode = "written"
    else:
        baseline = _load_json(path)
        mode = "compared"
    status_changed = baseline.get("status") != current.get("status")
    return redact_payload(
        {
            "status": "warn" if status_changed else "ok",
            "mode": mode,
            "baseline_path": str(path),
            "baseline_status": baseline.get("status", "missing"),
            "current_status": current.get("status", "unknown"),
            "status_changed": status_changed,
            "blocker_delta": len(current.get("blockers", [])) - len(baseline.get("blockers", [])),
            "warning_delta": len(current.get("warnings", [])) - len(baseline.get("warnings", [])),
            "live_trading_enabled": False,
        }
    )


def report_index(settings: BotSettings) -> dict[str, Any]:
    root = settings.data_dir / "reports" / "operator"
    reports: list[dict[str, Any]] = []
    if root.exists():
        for path in sorted(root.glob("operator-report.*")):
            if path.is_file():
                reports.append({"path": str(path), "suffix": path.suffix.lower(), "size_bytes": path.stat().st_size, "updated_at": int(path.stat().st_mtime)})
    comparison = {"status": "empty" if not reports else "single" if len(reports) == 1 else "available", "reports": len(reports)}
    return redact_payload({"status": "ok", "reports": reports, "comparison": comparison, "live_trading_enabled": False})


def verify_support_bundles(settings: BotSettings) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for path in sorted((settings.data_dir / "support").glob("*.zip")):
        rows.append(verify_support_bundle(path))
    return redact_payload({"status": "fail" if any(row.get("status") != "ok" for row in rows) else "ok", "bundles": rows, "count": len(rows), "live_trading_enabled": False})


def redaction_self_test() -> dict[str, Any]:
    sample_value = "abcdefghijklmnopqrstuvwxyz" + "1234567890"
    samples = {
        "binance_json_secret": '{"api_secret":"' + sample_value + '"}',
        "binance_env_key": "BINANCE_API_KEY=" + sample_value,
        "openai": "sk-" + ("a" * 30),
        "token_like": "A" * 64,
    }
    redacted = {name: redact_text(value) for name, value in samples.items()}
    leaked = [name for name, value in redacted.items() if sample_value in value or "sk-" in value or ("A" * 64) in value]
    return {"status": "fail" if leaked else "ok", "checked": len(samples), "leaked": leaked, "live_trading_enabled": False}


def operator_command_manifest() -> dict[str, Any]:
    commands = [
        ("diagnostics", "Collect local runtime health."),
        ("support-bundle", "Create a redacted support archive."),
        ("support-bundle-verify", "Verify one support archive."),
        ("support-bundle-restore-preview", "Preview bundle contents without extraction."),
        ("retention-preview", "Preview local artifact retention."),
        ("state-archive", "Create a preview-only state archive."),
        ("incident-timeline", "Show local operator incident events."),
        ("operator-report", "Export a local operator report."),
        ("operator-report-diff", "Diff the last two operator reports."),
        ("operator-quality-gate", "Run the local operator gate."),
        ("operator-health-score", "Score local operator health."),
        ("artifact-catalog", "List and filter local artifacts."),
        ("diagnostics-baseline", "Write or compare diagnostics baseline."),
        ("report-index", "Index local operator reports."),
        ("support-bundles-verify", "Verify all local support bundles."),
        ("redaction-self-test", "Validate secret redaction."),
        ("local-ops-snapshot", "Export full local ops snapshot."),
        ("evidence-manifest", "Write evidence manifest."),
        ("evidence-chain", "Write chained evidence hashes."),
        ("environment-doctor", "Check Python, packages, and paths."),
        ("data-growth-budget", "Summarize local data growth budget."),
        ("rehearsal-profiles", "List fast, standard, and deep rehearsals."),
        ("demo-acceptance-rehearsal", "Run demo acceptance rehearsal."),
    ]
    return {
        "status": "ok",
        "commands": [{"command": name, "purpose": purpose, "live_trading": False} for name, purpose in commands],
        "live_trading_enabled": False,
    }


def write_evidence_manifest(settings: BotSettings) -> dict[str, Any]:
    path = settings.data_dir / "evidence" / "manifest" / "latest-evidence-manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "ok",
        "diagnostics": OperatorDiagnostics(settings).state_health().to_dict(),
        "artifact_catalog": artifact_catalog(settings),
        "reports": report_index(settings),
        "live_trading_enabled": False,
    }
    path.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return {"status": "ok", "path": str(path), "live_trading_enabled": False}


def local_ops_snapshot(settings: BotSettings) -> dict[str, Any]:
    return redact_payload(
        {
            "status": "ok",
            "health_score": operator_health_score(settings),
            "diagnostics": OperatorDiagnostics(settings).state_health().to_dict(),
            "baseline": diagnostics_baseline(settings),
            "artifact_catalog": artifact_catalog(settings),
            "rehearsal_profiles": rehearsal_profiles(),
            "retention": retention_preview(settings),
            "timeline": incident_timeline(settings),
            "reports": report_index(settings),
            "report_diff": operator_report_diff(settings),
            "support_bundles": verify_support_bundles(settings),
            "environment_doctor": environment_doctor(settings),
            "data_growth_budget": data_growth_budget(settings),
            "redaction_self_test": redaction_self_test(),
            "command_manifest": operator_command_manifest(),
            "live_trading_enabled": False,
        }
    )


def retention_preview(settings: BotSettings, *, older_than_days: int = 7) -> dict[str, Any]:
    cutoff = time.time() - older_than_days * 24 * 60 * 60
    rows: list[dict[str, Any]] = []
    for name in RETENTION_ROOTS:
        root = settings.data_dir / name
        if not root.exists():
            rows.append({"root": name, "path": str(root), "exists": False, "old_files": 0, "size_bytes": 0})
            continue
        files = [path for path in root.rglob("*") if path.is_file()]
        old = [path for path in files if path.stat().st_mtime < cutoff]
        rows.append(
            {
                "root": name,
                "path": str(root),
                "exists": True,
                "files": len(files),
                "old_files": len(old),
                "size_bytes": sum(path.stat().st_size for path in files),
            }
        )
    return redact_payload({"status": "ok", "older_than_days": older_than_days, "items": rows, "live_trading_enabled": False})


def create_state_archive(settings: BotSettings, output_zip: Path, *, older_than_days: int = 7) -> dict[str, Any]:
    preview = retention_preview(settings, older_than_days=older_than_days)
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("retention-preview.json", json.dumps(preview, indent=2, default=str))
        archive.writestr("archive-manifest.json", json.dumps({"mode": "preview-only", "live_trading_enabled": False}, indent=2))
    return {"status": "ok", "archive": str(output_zip), "mode": "preview-only", "live_trading_enabled": False}


def incident_timeline(settings: BotSettings, *, limit: int = 50) -> list[dict[str, Any]]:
    data_dir = settings.data_dir
    events: list[dict[str, Any]] = []
    candidates = [
        ("diagnostics", data_dir / "evidence" / "diagnostics" / "latest-diagnostics.json"),
        ("scorecard", data_dir / "evidence" / "scorecards" / "latest-scorecard.json"),
        ("rehearsal", data_dir / "evidence" / "rehearsals" / "latest.json"),
        ("launch", data_dir / "checks" / "dashboard" / "launch-evidence.json"),
        ("pilot_idempotency", data_dir / "evidence" / "pilot-start-idempotency.json"),
    ]
    for kind, path in candidates:
        payload = _load_json(path)
        if payload:
            events.append(
                {
                    "timestamp_ms": int(payload.get("generated_at_ms") or payload.get("finished_at_ms") or path.stat().st_mtime * 1000),
                    "kind": kind,
                    "status": payload.get("status", "unknown"),
                    "path": str(path),
                }
            )
    for path in sorted((data_dir / "pilot-runs").glob("*/pilot-run.json")):
        payload = _load_json(path)
        if payload:
            events.append(
                {
                    "timestamp_ms": int(payload.get("updated_at_ms") or payload.get("started_at_ms") or path.stat().st_mtime * 1000),
                    "kind": "pilot_run",
                    "status": payload.get("state", "unknown"),
                    "path": str(path),
                }
            )
    return redact_payload(sorted(events, key=lambda row: row["timestamp_ms"])[-limit:])


def write_timeline_markdown(settings: BotSettings) -> Path:
    path = settings.data_dir / "reports" / "operator" / "incident-timeline.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = incident_timeline(settings)
    lines = ["# Operator Incident Timeline", "", "| Timestamp ms | Kind | Status | Path |", "| --- | --- | --- | --- |"]
    lines.extend(f"| {row['timestamp_ms']} | {row['kind']} | {row['status']} | {row['path']} |" for row in rows)
    path.write_text(redact_text("\n".join(lines) + "\n"), encoding="utf-8")
    return path


def export_operator_report(settings: BotSettings) -> dict[str, str]:
    diagnostics = OperatorDiagnostics(settings)
    diag_payload = diagnostics.state_health().to_dict()
    trend = diagnostics.trend_summary()
    retention = retention_preview(settings)
    timeline = incident_timeline(settings)
    out_dir = settings.data_dir / "reports" / "operator"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "operator-report.md"
    html_path = out_dir / "operator-report.html"
    md = _report_markdown(diag_payload, trend, retention, timeline)
    md_path.write_text(redact_text(md), encoding="utf-8")
    html_path.write_text(_html(md), encoding="utf-8")
    return {"markdown": str(md_path), "html": str(html_path), "live_trading_enabled": "false"}


def operator_quality_gate(settings: BotSettings) -> dict[str, Any]:
    diagnostics = OperatorDiagnostics(settings)
    diag = diagnostics.state_health().to_dict()
    report = export_operator_report(settings)
    bundle = create_support_bundle(settings, settings.data_dir / "support" / "quality-gate-support.zip")
    verify = verify_support_bundle(Path(bundle["bundle"]))
    findings = scan_for_secrets(settings.data_dir.parent if settings.data_dir.parent else settings.data_dir)
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    if diag.get("status") == "fail":
        blockers.extend(diag.get("blockers", []))
    elif diag.get("status") == "warn":
        warnings.extend(diag.get("warnings", []))
    if verify.get("status") != "ok":
        blockers.append({"name": "support_bundle.verify", "message": "support bundle verification failed"})
    if findings:
        blockers.append({"name": "security_scan.findings", "message": f"{len(findings)} possible secrets"})
    status = "fail" if blockers else "warn" if warnings else "ok"
    return redact_payload(
        {
            "status": status,
            "blockers": blockers,
            "warnings": warnings,
            "diagnostics_status": diag.get("status"),
            "report": report,
            "support_bundle": bundle,
            "support_bundle_verify": verify,
            "live_trading_enabled": False,
        }
    )


def _report_markdown(diag: dict[str, Any], trend: dict[str, Any], retention: dict[str, Any], timeline: list[dict[str, Any]]) -> str:
    lines = [
        "# Local Operator Report",
        "",
        "Live trading: disabled",
        f"Diagnostics status: {diag.get('status', 'unknown')}",
        f"Diagnostics trend points: {trend.get('points', 0)}",
        "",
        "## Recommended Actions",
    ]
    lines.extend(f"- {row.get('action', '-')}" for row in diag.get("recommended_actions", []))
    lines.extend(["", "## Retention Preview"])
    lines.extend(f"- {row.get('root')}: {row.get('files', 0)} files, {row.get('old_files', 0)} old" for row in retention.get("items", []))
    lines.extend(["", "## Timeline"])
    lines.extend(f"- {row.get('timestamp_ms')} {row.get('kind')} {row.get('status')}" for row in timeline)
    return "\n".join(lines) + "\n"


def _html(markdown: str) -> str:
    body = "<br>\n".join(html.escape(line) for line in markdown.splitlines())
    return f"<!doctype html><html><body><pre>{body}</pre></body></html>"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {"value": payload}


def _catalog_summaries(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_category: dict[str, dict[str, int]] = {}
    by_suffix: dict[str, int] = {}
    stale = 0
    for row in rows:
        category = str(row.get("category", "unknown"))
        suffix = str(row.get("suffix", ""))
        by_suffix[suffix] = by_suffix.get(suffix, 0) + 1
        bucket = by_category.setdefault(category, {"count": 0, "size_bytes": 0})
        bucket["count"] += 1
        bucket["size_bytes"] += int(row.get("size_bytes", 0))
        if row.get("stale"):
            stale += 1
    return {"by_category": by_category, "by_suffix": by_suffix, "stale": stale, "stale_count": stale}


def _format_digest(digest: str) -> str:
    return "-".join(digest[index : index + 8] for index in range(0, len(digest), 8))


def _can_write(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True
    except OSError:
        return False
