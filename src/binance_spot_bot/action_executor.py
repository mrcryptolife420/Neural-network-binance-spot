from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from .action_policy import validate_action_proposal
from .action_proposals import ActionProposal, ActionStatus, proposal_from_command
from .approval_queue import ApprovalQueueStore
from .local_job_runner import run_local_job
from .redaction import redact_payload

Runner = Callable[[str], dict[str, Any]]


@dataclass(frozen=True)
class ExecutionResult:
    execution_id: str
    proposal_id: str
    started_at_ms: int
    finished_at_ms: int
    status: str
    exit_code: int = 0
    stdout_path: str = ""
    stderr_path: str = ""
    artifacts: list[str] = field(default_factory=list)
    redacted: bool = True
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload({**asdict(self), "redacted": True, "live_trading_enabled": False})


class ActionExecutor:
    def __init__(self, root: Path | str, *, data_dir: Path | str | None = None, runner: Runner | None = None) -> None:
        self.root = Path(root)
        self.action_root = self.root / "action-center"
        self.queue = ApprovalQueueStore(self.action_root)
        self.executions_dir = self.action_root / "executions"
        self.executions_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir = Path(data_dir or root)
        self.runner = runner

    def execute(self, proposal_id: str, *, execute_process: bool = False) -> dict[str, Any]:
        record = self.queue.load(proposal_id)
        if record.status != ActionStatus.APPROVED.value:
            return {"status": "blocked", "reason": "proposal_not_approved", "live_trading_enabled": False}
        validation = validate_action_proposal(record.proposal, data_dir=self.data_dir)
        if not validation.allowed:
            return {"status": "blocked", "validation": validation.to_dict(), "live_trading_enabled": False}
        self.queue.update_status(proposal_id, ActionStatus.EXECUTING.value, reason="execution_started")
        result = self._run(record.proposal, execute_process=execute_process)
        self._write_result(result)
        self.queue.link_execution(proposal_id, result.execution_id)
        self.queue.update_status(proposal_id, ActionStatus.EXECUTED.value if result.status == "executed" else ActionStatus.VERIFICATION_FAILED.value)
        return result.to_dict()

    def _run(self, proposal: ActionProposal, *, execute_process: bool) -> ExecutionResult:
        started = int(time.time() * 1000)
        execution_id = f"exec-{proposal.proposal_id}-{started}"
        command = proposal.command.preview()
        if self.runner:
            raw = self.runner(command)
        elif execute_process:
            raw = run_local_job(command, root=self.root, execute=True, cwd=Path.cwd())
        else:
            raw = {"status": "executed", "returncode": 0, "stdout": f"dry-run safe execution for {command}", "stderr": ""}
        finished = int(time.time() * 1000)
        stdout = str(raw.get("stdout", raw.get("stdout_tail", "")))
        stderr = str(raw.get("stderr", raw.get("stderr_tail", "")))
        stdout_path = self.executions_dir / f"{execution_id}.stdout.txt"
        stderr_path = self.executions_dir / f"{execution_id}.stderr.txt"
        stdout_path.write_text(str(redact_payload(stdout)), encoding="utf-8")
        stderr_path.write_text(str(redact_payload(stderr)), encoding="utf-8")
        status = "executed" if raw.get("status") in {"ok", "ready", "executed"} and int(raw.get("returncode", raw.get("exit_code", 0)) or 0) == 0 else "failed"
        return ExecutionResult(
            execution_id=execution_id,
            proposal_id=proposal.proposal_id,
            started_at_ms=started,
            finished_at_ms=finished,
            status=status,
            exit_code=int(raw.get("returncode", raw.get("exit_code", 0)) or 0),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            artifacts=[str(stdout_path), str(stderr_path)],
        )

    def _write_result(self, result: ExecutionResult) -> Path:
        path = self.executions_dir / f"{result.execution_id}.json"
        path.write_text(json.dumps(result.to_dict(), indent=2, default=str), encoding="utf-8")
        return path


def execute_approved_action(action_type: str, approved: bool) -> dict[str, Any]:
    proposal = proposal_from_command(_legacy_action_to_command(action_type), title=action_type)
    if not approved:
        return {"status": "blocked", "reason": "approval_required", "live_trading_enabled": False}
    validation = validate_action_proposal(proposal)
    if not validation.allowed:
        return {"status": "blocked", "validation": validation.to_dict(), "live_trading_enabled": False}
    return {
        "status": "executed",
        "action_type": action_type,
        "execution": "dry_run_safe_local_action",
        "requires_manual_click": True,
        "redacted": True,
        "live_trading_enabled": False,
    }


def _legacy_action_to_command(action_type: str) -> str:
    return {
        "export_report": "operator-report",
        "create_support_bundle": "support-bundle",
        "pause_paper_runner": "pilot-runner-stop",
        "reconcile_orders": "pilot-status",
    }.get(action_type, action_type)
