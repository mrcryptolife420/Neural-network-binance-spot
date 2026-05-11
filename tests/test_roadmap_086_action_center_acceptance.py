from __future__ import annotations

import json
from pathlib import Path

from binance_spot_bot.action_audit_bundle import export_action_audit_bundle, verify_action_audit_bundle
from binance_spot_bot.action_executor import ActionExecutor, execute_approved_action
from binance_spot_bot.action_policy import validate_action_proposal
from binance_spot_bot.action_proposals import (
    ActionEvidenceLink,
    ActionExpectedOutcome,
    ActionSafetyClass,
    action_proposal_from_ai_ops,
    proposal_from_command,
)
from binance_spot_bot.action_verification import ActionVerifier
from binance_spot_bot.approval_plans import approval_plan
from binance_spot_bot.approval_queue import ApprovalQueueStore
from binance_spot_bot.approval_workflow import ApprovalWorkflow
from binance_spot_bot.decision_journal import DecisionJournal
from binance_spot_bot.decision_outcome_analytics import decision_outcome_analytics
from binance_spot_bot.local_operator_identity import can_operator, local_operator_identity
from binance_spot_bot.runbook_action_workflow import runbook_action_workflow


def test_action_policy_blocks_live_orders_sensitive_values_and_injection(tmp_path: Path) -> None:
    safe = proposal_from_command("diagnostics", ["--json"], expected_outputs=[ActionExpectedOutcome("json", str(tmp_path / "report.json"))])
    live = proposal_from_command("demo-execution-place", ["--armed"], safety_class=ActionSafetyClass.FORBIDDEN)
    blocked_sensitive = proposal_from_command("diagnostics", ["x" * 60])
    injected = proposal_from_command("diagnostics", ["--json", ";", "whoami"])

    assert validate_action_proposal(safe, data_dir=tmp_path).allowed is True
    assert validate_action_proposal(live, data_dir=tmp_path).allowed is False
    assert "forbidden" in " ".join(validate_action_proposal(live, data_dir=tmp_path).reasons)
    assert "secret_like_action_payload" in validate_action_proposal(blocked_sensitive, data_dir=tmp_path).reasons
    assert "shell_injection_token" in validate_action_proposal(injected, data_dir=tmp_path).reasons


def test_approval_queue_workflow_journal_execute_verify(tmp_path: Path) -> None:
    workflow = ApprovalWorkflow(tmp_path, data_dir=tmp_path)
    proposal = proposal_from_command("diagnostics", ["--json"], title="Diagnostics")
    submitted = workflow.submit(proposal)
    approved = workflow.decide(proposal.proposal_id, "approve", reason="safe read-only")

    assert submitted["status"] == "proposed"
    assert approved["approved"] is True

    executor = ActionExecutor(tmp_path, data_dir=tmp_path, runner=lambda _cmd: {"status": "ok", "returncode": 0, "stdout": "ok", "stderr": ""})
    execution = executor.execute(proposal.proposal_id)
    verification = ActionVerifier(tmp_path).verify(proposal.proposal_id, execution)

    assert execution["status"] == "executed"
    assert verification["status"] == "pass"
    assert ApprovalQueueStore(tmp_path / "action-center").load(proposal.proposal_id).status == "completed"
    assert DecisionJournal(tmp_path / "action-center").entries()


def test_confirm_evidence_and_forbidden_boundaries(tmp_path: Path) -> None:
    workflow = ApprovalWorkflow(tmp_path, data_dir=tmp_path)
    confirm = proposal_from_command(
        "metrics-compact",
        ["--confirm", "COMPACT_METRICS"],
        safety_class=ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED,
        confirm_phrase="COMPACT_METRICS",
    )
    blocked = workflow.submit(confirm)
    forbidden = proposal_from_command("withdraw", ["funds"], safety_class=ActionSafetyClass.FORBIDDEN)

    assert blocked["status"] in {"blocked", "needs_confirmation", "needs_evidence"}
    assert workflow.submit(forbidden)["status"] == "blocked"
    assert execute_approved_action("withdraw", approved=True)["status"] == "blocked"

    preview = tmp_path / "preview.json"
    preview.write_text("{}", encoding="utf-8")
    confirm_with_preview = proposal_from_command(
        "metrics-compact",
        ["--confirm", "COMPACT_METRICS"],
        safety_class=ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED,
        confirm_phrase="COMPACT_METRICS",
        required_evidence=[ActionEvidenceLink("preview-compaction", str(preview), "preview first")],
    )
    workflow.submit(confirm_with_preview)
    wrong = workflow.decide(confirm_with_preview.proposal_id, "approve", confirm_phrase="WRONG")
    right = workflow.decide(confirm_with_preview.proposal_id, "approve", confirm_phrase="COMPACT_METRICS")

    assert wrong["approved"] is False
    assert right["approved"] is True


def test_ai_ops_runbook_plans_identity_audit_analytics_and_report(tmp_path: Path) -> None:
    ai = action_proposal_from_ai_ops({"cmd": "python -m binance_spot_bot.cli diagnostics --json", "reason": "check status"})
    runbook = runbook_action_workflow("support-bundle")
    plan = approval_plan(["export_report", "create_support_bundle"])
    identity = local_operator_identity("alice", "maintainer")
    analytics = decision_outcome_analytics([{"decision": "approve", "next_status": "completed", "execution_status": "executed", "verification_status": "pass"}])
    source = tmp_path / "decision-journal.jsonl"
    source.write_text(json.dumps({"decision": "approve", "live_trading_enabled": False}), encoding="utf-8")
    bundle = export_action_audit_bundle([source], tmp_path / "bundles")
    verified = verify_action_audit_bundle(Path(bundle["manifest"]))

    assert ai.source == "ai_ops"
    assert runbook["proposals"]
    assert plan["status"] == "waiting_for_approval"
    assert identity["identity"]["role"] == "maintainer"
    assert can_operator("maintainer", "execute_approved") is True
    assert can_operator("admin_local", "live_trading") is False
    assert analytics["verification_pass_rate"] == 1.0
    assert bundle["redaction_proof"] is True
    assert verified["status"] == "ok"
