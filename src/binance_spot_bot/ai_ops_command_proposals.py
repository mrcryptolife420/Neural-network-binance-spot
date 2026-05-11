from __future__ import annotations

from typing import Any

from .ai_ops_guidance_policy import guidance_policy
from .local_job_allowlist import validate_local_job_command


def propose_ai_ops_command(command: str, *, reason: str = "operator guidance") -> dict[str, Any]:
    validation = validate_local_job_command(command)
    policy = guidance_policy(command)
    allowed = validation.allowed and policy["safety_class"] != "forbidden"
    return {
        "status": "ready" if allowed else "blocked",
        "command": f"python -m binance_spot_bot.cli {command}" if not command.startswith("python") else command,
        "args": validation.args,
        "safety_class": policy["safety_class"],
        "reason": reason,
        "expected_output": "local redacted JSON/report output",
        "requires_confirmation": policy["safety_class"] == "confirm_required",
        "confirm_phrase": policy.get("confirm_phrase", ""),
        "forbidden_if": validation.reasons,
        "related_runbook": "failed-scheduled-report" if "support" in command else "morning-check",
        "no_auto_execute": True,
        "live_trading_enabled": False,
    }
