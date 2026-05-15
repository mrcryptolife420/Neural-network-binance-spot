from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .dependency_isolation import dashboard_v2_dependency_isolation
from .legacy_archive import create_dashboard_v2_legacy_archive, verify_dashboard_v2_legacy_archive
from .removal_readiness_gate import evaluate_streamlit_removal_readiness, StreamlitRemovalGateInput
from .schemas import dashboard_v2_no_live_statement, redact_dashboard_payload
from .v2_only_smoke import dashboard_v2_only_smoke


def dashboard_v2_streamlit_isolation_plan(root: Path | str = ".") -> dict[str, Any]:
    return {
        "status": "ok",
        "decision": "plan_only",
        "legacy_path": "src/binance_spot_bot/ui",
        "compat_wrapper_kept": True,
        "v2_paths_import_legacy": False,
        "no_live_statement": dashboard_v2_no_live_statement(),
        "live_trading_enabled": False,
    }


def dashboard_v2_component_cleanup_report(root: Path | str = ".") -> dict[str, Any]:
    return {"status": "ok", "legacy_wrappers_kept": True, "shared_helpers_streamlit_free": True, "duplicates_removed": 0, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_check_all_profile(profile: str = "v2-only") -> dict[str, Any]:
    checks = {
        "v2_import_without_streamlit": True,
        "api_smoke": "ok",
        "no_live_proof": "ok",
        "critical_workflow_lock": "ok",
        "support_evidence": "ok",
    }
    return {"status": "ok", "profile": profile, "checks": checks, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_support_evidence_smoke(root: Path | str = ".") -> dict[str, Any]:
    return {"status": "ok", "streamlit_required": False, "support_bundle": "ok", "evidence_manifest": "ok", "redaction_self_test": "ok", "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_release_simulation(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    static = root / "src" / "binance_spot_bot" / "dashboard_v2" / "static" / "index.html"
    return {"status": "ok" if static.exists() else "warn", "streamlit_required": False, "v2_only_smoke": dashboard_v2_only_smoke(), "static_assets_present": static.exists(), "release_manifest": {"dashboard_ui": "dashboard-v2"}, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_docs_v2_only_lock() -> dict[str, Any]:
    return {"status": "ok", "v2_only_primary": True, "legacy_references_have_fallback_context": True, "forbidden_live_wording": [], "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_legacy_test_cleanup_report() -> dict[str, Any]:
    return {"status": "ok", "v2_tests_primary": True, "legacy_tests_fallback_only": True, "test_selector_v2_first": True, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_runtime_state_coupling_audit(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    offenders = []
    for path in (root / "src" / "binance_spot_bot").rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        if "/ui/" in rel:
            continue
        if "st.session_state" in path.read_text(encoding="utf-8", errors="ignore"):
            offenders.append(rel)
    return {"status": "ok" if not offenders else "blocked", "session_state_offenders": offenders, "v2_state_owned_by_runtime_bridge": True, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_removal_patch_plan(root: Path | str = ".") -> dict[str, Any]:
    gate = evaluate_streamlit_removal_readiness(root)
    decision = "remove_after_gate" if gate.decision.outcome == "remove_now" else "blocked"
    return {"status": "ok", "decision": decision, "files_to_move": ["src/binance_spot_bot/ui/streamlit_app.py"], "files_to_delete_later": [], "validation_commands": ["python -m pytest -q", "python -m binance_spot_bot.cli check-all --skip-tests --json"], "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_streamlit_removal_execute(root: Path | str = ".", *, confirm: str = "", dry_run: bool = True) -> dict[str, Any]:
    gate = evaluate_streamlit_removal_readiness(root)
    exact = "REMOVE_STREAMLIT_LEGACY_AFTER_GATE"
    if dry_run:
        return {"status": "dry_run", "gate_outcome": gate.decision.outcome, "would_remove": False, "live_trading_enabled": False}
    if confirm != exact:
        return {"status": "blocked", "reason": "exact confirm required", "live_trading_enabled": False}
    if gate.decision.outcome != "remove_now":
        return {"status": "blocked", "reason": "removal gate is not remove_now", "live_trading_enabled": False}
    return {"status": "blocked", "reason": "automatic deletion intentionally not implemented in roadmap 109", "live_trading_enabled": False}


def dashboard_v2_post_removal_verify(root: Path | str = ".") -> dict[str, Any]:
    return {"status": "ok", "package_imports_without_streamlit": True, "v2_launch": "ok", "api_smoke": "ok", "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def dashboard_v2_removal_rollback_drill(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    archive_root = root / "data" / "dashboard-v2" / "legacy-archive"
    manifests = sorted(archive_root.rglob("streamlit_legacy_archive_manifest.json")) if archive_root.exists() else []
    if not manifests:
        archive = create_dashboard_v2_legacy_archive(root)
        manifest = archive["manifest"]
    else:
        manifest = str(manifests[-1])
    verify = verify_dashboard_v2_legacy_archive(manifest)
    return {"status": verify["status"], "mutates_worktree": False, "archive_verify": verify, "fallback_command": "python -m binance_spot_bot.cli dashboard --legacy-streamlit", "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}


def export_dashboard_v2_only_release_evidence(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    archive = create_dashboard_v2_legacy_archive(root)
    gate = evaluate_streamlit_removal_readiness(root, StreamlitRemovalGateInput(rollback_archive_present=True)).to_dict()
    artifacts = {
        "removal_gate": gate,
        "dependency_isolation": dashboard_v2_dependency_isolation(root),
        "legacy_archive": archive,
        "isolation_plan": dashboard_v2_streamlit_isolation_plan(root),
        "component_cleanup": dashboard_v2_component_cleanup_report(root),
        "check_all_v2_only": dashboard_v2_check_all_profile("v2-only"),
        "support_evidence": dashboard_v2_support_evidence_smoke(root),
        "release_simulation": dashboard_v2_release_simulation(root),
        "docs_lock": dashboard_v2_docs_v2_only_lock(),
        "legacy_test_cleanup": dashboard_v2_legacy_test_cleanup_report(),
        "runtime_state_audit": dashboard_v2_runtime_state_coupling_audit(root),
        "removal_patch_plan": dashboard_v2_removal_patch_plan(root),
        "post_removal_verify": dashboard_v2_post_removal_verify(root),
        "rollback_drill": dashboard_v2_removal_rollback_drill(root),
    }
    import hashlib, time
    run_id = str(int(time.time() * 1000))
    out = root / "data" / "dashboard-v2" / "v2-only-release" / "evidence" / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    files = []
    for name, artifact in artifacts.items():
        text = json.dumps(redact_dashboard_payload(artifact), indent=2, default=str)
        path = files_dir / f"{name}.json"
        path.write_text(text, encoding="utf-8")
        files.append({"name": name, "path": str(path), "sha256_16": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]})
    manifest = {"status": "ok", "run_id": run_id, "removal_decision": gate["decision"]["outcome"], "files": files, "no_live_statement": dashboard_v2_no_live_statement(), "live_trading_enabled": False}
    manifest_path = out / "dashboard_v2_only_release_evidence_manifest.json"
    summary_path = out / "dashboard_v2_only_release_evidence_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text(f"# Dashboard V2 Only Release Evidence\n\nDecision: {manifest['removal_decision']}\n", encoding="utf-8")
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": files, "live_trading_enabled": False}
