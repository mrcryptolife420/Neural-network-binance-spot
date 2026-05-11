from __future__ import annotations

import re
import shlex
from dataclasses import dataclass, field
from typing import Any

from .redaction import redact_payload

ALLOWED_LOCAL_OPS_COMMANDS = {
    "diagnostics",
    "support-bundle",
    "support-bundle-verify",
    "support-bundles-verify",
    "operator-report",
    "operator-quality-gate",
    "operator-health-score",
    "artifact-catalog",
    "evidence-chain",
    "evidence-manifest",
    "report-index",
    "redaction-self-test",
    "local-ops-snapshot",
    "dashboard-smoke",
    "dashboard-browser-smoke",
    "paper-session",
    "paper-deployment-cycle",
    "data-quality",
    "weekly-governance-report",
    "governance-evidence-bundle",
    "governance-simulation",
    "ab-paper-status",
    "data-growth-budget",
    "retention-preview",
    "state-archive",
    "local-job-list",
    "local-scheduler-tick",
    "scheduled-report-plan",
    "runbook-list",
    "governance-reminders",
    "paper-ops-calendar",
    "runbook-drill",
    "metrics-ingest",
    "metrics-query",
    "metrics-latest",
    "metrics-aggregate",
    "metrics-slo",
    "metrics-anomalies",
    "metrics-export",
    "metrics-compact",
    "ai-ops-ask",
    "ai-ops-context",
    "ai-ops-search",
    "ai-ops-runbook",
    "ai-ops-command-proposal",
    "ai-ops-safety-test",
    "ai-ops-export-session",
}
FORBIDDEN_COMMANDS = {
    "demo-execution-place",
    "demo-execution-cancel",
    "demo-execution-query",
    "demo-execution-test-order",
    "connectivity-check",
}
FORBIDDEN_TOKENS = {"live", "--live", "armed", "--armed", "withdraw", "order", "account", "signature", "listenKey"}
SHELL_INJECTION = re.compile(r"[;&|`<>$()]")
SECRET_LIKE = re.compile(r"(?i)(api[_-]?key|api[_-]?secret|secret|signature|listenkey)|[A-Za-z0-9_-]{56,}")


@dataclass(frozen=True)
class LocalJobValidation:
    allowed: bool
    command: str
    args: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                "allowed": self.allowed,
                "command": self.command,
                "args": self.args,
                "reasons": self.reasons,
                "live_trading_enabled": False,
            }
        )


def parse_local_command(command: str, args: list[str] | None = None) -> tuple[str, list[str]]:
    tokens = shlex.split(command, posix=False) if isinstance(command, str) else list(command)
    tokens.extend(args or [])
    tokens = [token.strip("\"'") for token in tokens if token.strip()]
    if len(tokens) >= 3 and tokens[0].endswith("python") and tokens[1:3] == ["-m", "binance_spot_bot.cli"]:
        tokens = tokens[3:]
    if tokens and tokens[0] == "spot-bot":
        tokens = tokens[1:]
    if not tokens:
        return "", []
    return tokens[0], tokens[1:]


def validate_local_job_command(command: str, args: list[str] | None = None) -> LocalJobValidation:
    reasons: list[str] = []
    if SHELL_INJECTION.search(command) or any(SHELL_INJECTION.search(arg) for arg in (args or [])):
        reasons.append("shell_injection_token")
    cmd, parsed_args = parse_local_command(command, args)
    if cmd not in ALLOWED_LOCAL_OPS_COMMANDS:
        reasons.append("command_not_allowlisted")
    if cmd in FORBIDDEN_COMMANDS:
        reasons.append("forbidden_trading_command")
    lowered = [cmd.lower(), *[arg.lower() for arg in parsed_args]]
    if any(token in lowered for token in FORBIDDEN_TOKENS):
        reasons.append("forbidden_live_or_trading_token")
    joined = " ".join([command, *(args or [])])
    if SECRET_LIKE.search(joined):
        reasons.append("secret_like_argument")
    if cmd == "paper-session" and any(arg in {"--mode", "live"} for arg in parsed_args):
        reasons.append("paper_session_must_not_use_live_mode")
    return LocalJobValidation(not reasons, cmd, parsed_args, sorted(set(reasons)), False)


def is_safe_command(command: str) -> bool:
    return validate_local_job_command(command).allowed


def is_safe_cmd(command: str) -> bool:
    return is_safe_command(command)
