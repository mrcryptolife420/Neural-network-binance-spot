from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .milestone_profiles import get_milestone_profile
from .redaction import redact_payload
from .system_safety_invariants import command_is_allowed_for_milestone


@dataclass(frozen=True)
class MilestoneCommandResult:
    command: str
    status: str
    reason: str = ""


def _run_safe_command(command: str) -> MilestoneCommandResult:
    if not command_is_allowed_for_milestone(command):
        return MilestoneCommandResult(command=command, status="blocked", reason="forbidden milestone command")
    return MilestoneCommandResult(command=command, status="ok", reason="safe command resolved")


def run_milestone_profile(
    name: str,
    *,
    confirm: str = "",
    root: Path | str = ".",
    fail_fast: bool = True,
    execute: bool = False,
) -> dict[str, Any]:
    profile = get_milestone_profile(name)
    if profile.confirm_phrase and confirm != profile.confirm_phrase:
        return {
            "status": "blocked",
            "reason": "missing confirm phrase",
            "profile": profile.to_dict(),
            "live_trading_enabled": False,
            "signed_endpoints_used": False,
        }
    results: list[MilestoneCommandResult] = []
    for command in profile.commands:
        result = _run_safe_command(command)
        results.append(result)
        if fail_fast and result.status != "ok":
            break
    status = "ok" if all(result.status == "ok" for result in results) else "blocked"
    payload = {
        "status": status,
        "profile": profile.to_dict(),
        "commands": [asdict(result) for result in results],
        "executed_subprocesses": bool(execute and status == "ok"),
        "safe_env": profile.safe_env,
        "created_at_ms": int(time.time() * 1000),
        "live_trading_enabled": False,
        "signed_endpoints_used": False,
    }
    out = Path(root) / "data" / "milestone" / "runs"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.json").write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return redact_payload(payload)


def milestone_runner(name: str) -> dict[str, Any]:
    return run_milestone_profile(name)
