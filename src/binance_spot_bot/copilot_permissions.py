from __future__ import annotations

from dataclasses import asdict, dataclass


FORBIDDEN_ACTIONS = {"place_order", "cancel_order", "enable_live", "bypass_risk", "read_api_secret"}
READ_ONLY_ACTIONS = {"summarize_session", "explain_risk", "suggest_next_steps", "list_reports"}


@dataclass(frozen=True)
class PermissionDecision:
    action: str
    allowed: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def check_copilot_action(action: str) -> PermissionDecision:
    normalized = action.strip().lower()
    if normalized in FORBIDDEN_ACTIONS:
        return PermissionDecision(normalized, False, "copilot is read-only and cannot touch trading controls or secrets")
    if normalized in READ_ONLY_ACTIONS:
        return PermissionDecision(normalized, True, "read-only advisory action")
    return PermissionDecision(normalized, False, "unknown copilot action denied by default")
