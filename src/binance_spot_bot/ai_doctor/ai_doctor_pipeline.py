from __future__ import annotations

from pathlib import Path
from typing import Any

from .ai_context_pack import write_ai_context_pack
from .ai_summary_writer import write_ai_summary
from .check_all_capture import capture_check_all
from .codebase_context import collect_codebase_context
from .codex_prompt_writer import write_codex_fix_prompt
from .debug_pack_builder import build_debug_pack
from .doctor_evidence_bundle import export_ai_doctor_evidence
from .error_collector import collect_errors
from .finish_snapshot import collect_finish_snapshot
from .known_issue_matcher import match_known_issues
from .log_collector import collect_recent_logs
from .observer import append_ai_doctor_event
from .repair_suggestions import build_repair_suggestions
from .root_cause_hypotheses import build_root_cause_hypotheses
from .run_schema import ai_doctor_run_to_dict
from .start_snapshot import collect_start_snapshot
from .system_state_collector import collect_system_state


def run_ai_doctor_pipeline(root: Path, profile_id: str = "paper", error_text: str = "") -> dict[str, Any]:
    start = collect_start_snapshot(root, profile_id)
    run = start["run"]
    run_id = run.run_id
    event = append_ai_doctor_event(root, run_id, "dashboard_ready", {"status": "ok"})
    errors = collect_errors(root, run_id, error_text)
    logs = collect_recent_logs(root, run_id)
    system_state = collect_system_state(root, run_id)
    check_all = capture_check_all()
    codebase = collect_codebase_context(root, run_id, errors["errors"])
    issues = match_known_issues(errors["errors"])
    hypotheses = build_root_cause_hypotheses(issues["matches"])
    suspect_files = codebase["context"]["suspect_files"]
    summary = write_ai_summary(root, run_id, hypotheses["hypotheses"], suspect_files)
    prompt = write_codex_fix_prompt(root, run_id, issues["matches"], suspect_files)
    repairs = build_repair_suggestions(issues["matches"])
    context = write_ai_context_pack(root, summary["summary"], prompt["prompt"])
    finish = collect_finish_snapshot(root, run_id, "warning" if errors["errors"] else "ok", 0)
    debug_pack = build_debug_pack(root, run_id)
    evidence = export_ai_doctor_evidence(root, run_id, {"start": ai_doctor_run_to_dict(run), "event": event, "errors": errors, "logs": logs, "system_state": system_state, "check_all": check_all, "codebase": codebase, "issues": issues, "hypotheses": hypotheses, "summary": summary, "prompt": prompt, "repairs": repairs, "context": context, "finish": finish, "debug_pack": debug_pack})
    return {"status": "ok", "run_id": run_id, "start": ai_doctor_run_to_dict(run), "event": event, "errors": errors, "logs": logs, "system_state": system_state, "check_all": check_all, "codebase": codebase, "issues": issues, "hypotheses": hypotheses, "summary": summary, "prompt": prompt, "repairs": repairs, "context": context, "finish": finish, "debug_pack": debug_pack, "evidence": evidence, "live_trading_enabled": False, "live_order_submitted": False}

