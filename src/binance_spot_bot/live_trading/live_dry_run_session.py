from __future__ import annotations

from typing import Any

from .live_account_verifier import FakeLiveReadOnlyAdapter, verify_live_read_only_account
from .live_evidence_prerequisite_gate import evaluate_live_evidence_prerequisites, fixture_live_evidence
from .live_order_preview import build_live_order_preview
from .live_order_sizing_guard import evaluate_live_order_sizing


def run_live_dry_run_session(evidence: dict[str, Any] | None = None, *, adapter: FakeLiveReadOnlyAdapter | None = None, intent: dict[str, Any] | None = None) -> dict[str, Any]:
    evidence_report = evaluate_live_evidence_prerequisites(evidence or fixture_live_evidence())
    account = verify_live_read_only_account(adapter)
    preview = build_live_order_preview(intent or {"symbol": "BTCUSDT", "side": "BUY", "quote": 5})
    sizing = evaluate_live_order_sizing(preview, first_order_cap=10, max_balance_pct=0.10)
    blockers = evidence_report["blockers"] + account["blockers"] + preview.get("blockers", []) + sizing["blockers"]
    return {"status": "blocked" if blockers else "ok", "state": "dry_run_passed" if not blockers else "blocked", "evidence": evidence_report, "account": account, "preview": preview, "sizing": sizing, "expected_api_request_plan": ["server_time", "get_account_state", "local_order_preview"], "place_order_called": False, "blockers": blockers, "live_execution_enabled": False, "live_order_placement_enabled": False, "live_trading_enabled": False}
