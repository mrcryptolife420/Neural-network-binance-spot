from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class DashboardProcessStatus(str, Enum):
    NOT_STARTED = "not_started"
    STARTING = "starting"
    RUNNING = "running"
    UNREACHABLE = "unreachable"
    STOPPED = "stopped"


class BotEngineStatus(str, Enum):
    NOT_CREATED = "not_created"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass(frozen=True)
class DashboardRuntimeState:
    dashboard_status: DashboardProcessStatus
    bot_status: BotEngineStatus
    mode: str
    source: str
    profile: str
    live_disabled: bool = True

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["dashboard_status"] = self.dashboard_status.value
        payload["bot_status"] = self.bot_status.value
        return payload


def bot_status_from_runtime(status: str) -> BotEngineStatus:
    mapping = {
        "created": BotEngineStatus.READY,
        "running": BotEngineStatus.RUNNING,
        "ready": BotEngineStatus.READY,
        "stopped": BotEngineStatus.STOPPED,
        "completed": BotEngineStatus.COMPLETED,
    }
    return mapping.get(status, BotEngineStatus.ERROR)
