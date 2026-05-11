from __future__ import annotations

from pathlib import Path

from binance_spot_bot.action_proposals import ActionSafetyClass, proposal_from_command
from binance_spot_bot.approval_policy_templates import approval_policy_templates, validate_approval_template, ApprovalPolicyTemplate
from binance_spot_bot.compliance_bundle import export_compliance_bundle, verify_compliance_bundle
from binance_spot_bot.compliance_evidence import ComplianceEvidence, compliance_evidence_check
from binance_spot_bot.compliance_report import write_compliance_report
from binance_spot_bot.compliance_score import compliance_score
from binance_spot_bot.local_operator_identity import LocalOperatorIdentityStore
from binance_spot_bot.operator_roles import default_operator_roles
from binance_spot_bot.permission_change_workflow import approve_permission_change, propose_permission_change
from binance_spot_bot.permission_drift import permission_drift
from binance_spot_bot.permission_engine import can_approve, can_execute, evaluate_permission_for_operator
from binance_spot_bot.permission_profiles import FORBIDDEN_SCOPES, evaluate_permission, permission_matrix, write_permission_manifest
from binance_spot_bot.permission_review import permission_review
from binance_spot_bot.separation_of_duties import separation_of_duties


def test_identity_profiles_roles_and_permission_engine(tmp_path: Path) -> None:
    store = LocalOperatorIdentityStore(tmp_path / "identities")
    viewer = store.create_or_update("view", ["viewer"])
    operator = store.create_or_update("op", ["operator"])
    maintainer = store.create_or_update("maint", ["maintainer"])
    disabled = store.disable(operator.operator_id)
    destructive = proposal_from_command("metrics-compact", safety_class=ActionSafetyClass.DESTRUCTIVE_CONFIRM_REQUIRED)
    read_only = proposal_from_command("diagnostics", ["--json"])

    assert viewer.role == "viewer"
    assert evaluate_permission("operator", "start_demo")["allowed"] is True
    assert evaluate_permission("admin_local", "enable_live_trading")["allowed"] is False
    assert can_approve(viewer, read_only)["allowed"] is False
    assert can_approve(maintainer, destructive)["allowed"] is True
    assert can_execute(disabled, read_only)["allowed"] is False
    assert evaluate_permission_for_operator(maintainer, "execute_approved_action")["allowed"] is True
    assert permission_matrix()["live_trading_enabled"] is False
    assert default_operator_roles()["role_template_hash"]


def test_separation_templates_permission_change_and_drift(tmp_path: Path) -> None:
    assert separation_of_duties("alice", "alice", safety_class="destructive_confirm_required")["status"] == "blocked"
    assert separation_of_duties("alice", "bob", safety_class="destructive_confirm_required")["status"] == "ok"
    templates = approval_policy_templates()
    invalid = validate_approval_template(ApprovalPolicyTemplate("bad", "admin_local", ["forbidden"]))
    change = propose_permission_change("operator", {"scope": "view_reports"})
    bad_change = propose_permission_change("operator", {"scope": "enable_live_trading"})
    approved = approve_permission_change(change, role="admin_local", confirm="PERMISSION_CHANGE", out=tmp_path / "permission-change.json")
    drift = permission_drift({"operator": ["view_reports"]}, {"operator": ["view_reports", "enable_live_trading"]})

    assert templates["status"] == "ready"
    assert invalid["status"] == "blocked"
    assert change["status"] == "approval_required"
    assert bad_change["status"] == "blocked"
    assert approved["status"] == "ok"
    assert drift["status"] == "blocked"


def test_compliance_evidence_report_score_bundle_and_review(tmp_path: Path) -> None:
    manifest = write_permission_manifest(tmp_path)
    evidence = compliance_evidence_check([ComplianceEvidence("permission_manifest", str(manifest), status="ok")])
    report = write_compliance_report(tmp_path)
    score = compliance_score([{"required": True, "allowed": False}])
    blocked_score = compliance_score([{"required": True, "allowed": False, "hard_blocker": True}])
    bundle = export_compliance_bundle(tmp_path)
    verified = verify_compliance_bundle(Path(bundle["manifest"]))
    review = permission_review()

    assert evidence["status"] == "ok"
    assert report["no_live_proof"] is True
    assert score["status"] == "warn"
    assert blocked_score["status"] == "blocked"
    assert bundle["redaction_proof"] is True
    assert verified["status"] == "ok"
    assert review["live_trading_enabled"] is False
    assert "enable_live_trading" in FORBIDDEN_SCOPES
