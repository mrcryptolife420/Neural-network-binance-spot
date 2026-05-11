from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .action_proposals import ActionStatus
from .approval_queue import ApprovalQueueStore
from .redaction import redact_payload


@dataclass(frozen=True)
class VerificationCheck:
    name: str
    status: str
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class VerificationResult:
    verification_id: str
    execution_id: str
    proposal_id: str
    checks: list[VerificationCheck]
    status: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    next_action: str = ""
    timestamp_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(
            {
                **asdict(self),
                "checks": [check.to_dict() for check in self.checks],
                "live_trading_enabled": False,
            }
        )


def verify_action_result(action_type: str, result: dict) -> dict[str, Any]:
    status = "pass" if result.get("status") in {"executed", "ok"} and result.get("live_trading_enabled") is False else "fail"
    return {
        "status": status,
        "action_type": action_type,
        "checks": [{"name": "no-live proof", "status": "pass" if result.get("live_trading_enabled") is False else "fail"}],
        "live_trading_enabled": False,
    }


class ActionVerifier:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.action_root = self.root / "action-center"
        self.verification_dir = self.action_root / "verification"
        self.verification_dir.mkdir(parents=True, exist_ok=True)
        self.queue = ApprovalQueueStore(self.action_root)

    def verify(self, proposal_id: str, execution: dict[str, Any]) -> dict[str, Any]:
        checks = [
            VerificationCheck("execution completed", "pass" if execution.get("status") == "executed" else "fail"),
            VerificationCheck("no-live proof", "pass" if execution.get("live_trading_enabled") is False else "fail"),
            VerificationCheck("output redacted", "pass" if execution.get("redacted", True) else "fail"),
        ]
        for path_key in ("stdout_path", "stderr_path"):
            path = Path(str(execution.get(path_key, "")))
            if path_key in execution and str(path):
                checks.append(VerificationCheck(f"{path_key} exists", "pass" if path.exists() else "fail", str(path)))
        blockers = [check.name for check in checks if check.status == "fail"]
        status = "pass" if not blockers else "fail"
        verification = VerificationResult(
            verification_id=f"ver-{proposal_id}-{int(time.time() * 1000)}",
            execution_id=str(execution.get("execution_id", "")),
            proposal_id=proposal_id,
            checks=checks,
            status=status,
            blockers=blockers,
            next_action="" if status == "pass" else "create_follow_up_proposal",
        )
        path = self.verification_dir / f"{verification.verification_id}.json"
        path.write_text(json.dumps(verification.to_dict(), indent=2, default=str), encoding="utf-8")
        self.queue.link_verification(proposal_id, verification.verification_id)
        self.queue.update_status(proposal_id, ActionStatus.COMPLETED.value if status == "pass" else ActionStatus.VERIFICATION_FAILED.value)
        return {"path": str(path), **verification.to_dict()}
