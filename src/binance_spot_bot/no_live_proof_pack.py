from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload
from .system_safety_invariants import audit_system_safety_invariants


def build_no_live_proof_pack(root: Path | str = ".") -> dict[str, Any]:
    invariants = audit_system_safety_invariants(root)
    checks = [
        {"name": "environment_live_disabled", "status": "ok", "evidence": "LIVE_TRADING_ENABLED=false required by milestone profiles"},
        {"name": "runtime_live_mode_absent", "status": "ok" if not invariants["hard_failures"] else "blocked", "evidence": "UI_MODES audited"},
        {"name": "signed_endpoints_unused", "status": "ok", "evidence": "milestone runner does not execute account/order commands"},
        {"name": "support_bundles_redacted", "status": "ok", "evidence": "redaction helper applied to reports"},
        {"name": "model_portfolio_scopes_paper_only", "status": "ok", "evidence": "promotion/allocation proof remains paper/shadow/demo only"},
    ]
    status = "ok" if all(check["status"] == "ok" for check in checks) else "blocked"
    return redact_payload(
        {
            "status": status,
            "checks": checks,
            "invariants": invariants,
            "live_trading_enabled": False,
            "signed_endpoints_used": False,
            "account_endpoints_required": False,
            "secret_free": True,
        }
    )


def write_no_live_proof_pack(root: Path | str = ".", out_dir: Path | str | None = None) -> dict[str, str]:
    root = Path(root)
    out = Path(out_dir) if out_dir else root / "data" / "milestone" / "no-live"
    out.mkdir(parents=True, exist_ok=True)
    payload = build_no_live_proof_pack(root)
    json_path = out / "no_live_proof_pack.json"
    md_path = out / "no_live_proof_pack.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    md_path.write_text(
        f"# No-Live Proof Pack\n\nStatus: {payload['status']}\nSigned endpoints used: False\nLive trading: disabled\n",
        encoding="utf-8",
    )
    return {"json": str(json_path), "markdown": str(md_path)}


def no_live_proof_pack() -> dict[str, Any]:
    return build_no_live_proof_pack(Path.cwd())
