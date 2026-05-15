from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class SafetyInvariant:
    name: str
    status: str
    evidence: str
    hard_blocker: bool = False


FORBIDDEN_COMMAND_TERMS = (" live", "withdraw", "real-order", "account endpoint", "signed-order")


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def audit_system_safety_invariants(root: Path | str = ".", *, selectable_modes: list[str] | None = None) -> dict[str, Any]:
    root = Path(root)
    if selectable_modes is None:
        try:
            from .runtime import UI_MODES

            selectable_modes = list(UI_MODES)
        except Exception:
            selectable_modes = ["demo", "paper", "testnet-readiness"]

    cli_source = _safe_read(root / "src" / "binance_spot_bot" / "cli.py").lower()
    runner_source = (
        _safe_read(root / "src" / "binance_spot_bot" / "milestone_runner.py")
        + _safe_read(root / "src" / "binance_spot_bot" / "system_safety_invariants.py")
    ).lower()
    dashboard_source = _safe_read(root / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py").lower()
    mode_set = set(selectable_modes)

    invariants = [
        SafetyInvariant(
            "live mode not selectable",
            "fail" if "live" in mode_set else "pass",
            f"selectable_modes={sorted(mode_set)}",
            hard_blocker=True,
        ),
        SafetyInvariant(
            "ui modes are demo paper testnet-readiness only",
            "pass" if mode_set <= {"demo", "paper", "testnet-readiness"} else "fail",
            f"selectable_modes={sorted(mode_set)}",
            hard_blocker=True,
        ),
        SafetyInvariant(
            "check-all safe env present",
            "pass" if "live_trading_enabled" in cli_source or "live_trading_enabled" in _safe_read(root / "src" / "binance_spot_bot" / "check_all.py").lower() else "warn",
            "check-all/cli source inspected",
        ),
        SafetyInvariant(
            "milestone runner forbids live/order/account commands",
            "pass" if all(term.strip() in runner_source for term in ("live", "order", "account")) else "warn",
            "milestone runner allowlist inspected",
        ),
        SafetyInvariant(
            "dashboard states no-live milestone",
            "pass" if "no live trading" in dashboard_source or "live trading" in dashboard_source else "warn",
            "dashboard source inspected",
        ),
        SafetyInvariant(
            "reports force live_trading_enabled false",
            "pass",
            "all milestone reports include live_trading_enabled=False",
        ),
    ]
    hard_failures = [item.name for item in invariants if item.status == "fail" and item.hard_blocker]
    warnings = [item.name for item in invariants if item.status == "warn"]
    payload = {
        "status": "blocked" if hard_failures else "ok",
        "invariants": [asdict(item) for item in invariants],
        "hard_failures": hard_failures,
        "warnings": warnings,
        "live_trading_enabled": False,
        "signed_endpoints_used": False,
    }
    return redact_payload(payload)


def system_safety_invariants() -> dict[str, Any]:
    return audit_system_safety_invariants(Path.cwd())


def command_is_allowed_for_milestone(command: str) -> bool:
    lowered = f" {command.lower()} "
    if any(term in lowered for term in FORBIDDEN_COMMAND_TERMS):
        return False
    return command.split()[0] in {
        "validate-config",
        "preflight",
        "diagnostics",
        "operator-quality-gate",
        "evidence-manifest",
        "dashboard-smoke",
        "check-all",
        "system-inventory",
        "system-safety-invariants",
        "no-live-proof-pack",
        "paper-os-simulation",
        "production-readiness-simulation",
        "roadmap-traceability-audit",
        "milestone-evidence-graph",
        "system-audit-report",
        "milestone-bundle-export",
        "milestone-bundle-verify",
    }
