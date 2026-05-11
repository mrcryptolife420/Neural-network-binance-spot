from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import BotSettings
from .pilot_runner import PilotRunnerService
from .redaction import redact_payload
from .ui.chart_registry import all_chart_keys
from .ui.page_registry import PAGES


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class LaunchEvidence:
    timestamp: str
    status: str
    url: str
    port: int
    pid: int | None
    log_path: str
    error_log_path: str
    live_trading_enabled: bool
    kill_switch: bool
    preflight_status: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def dashboard_checks_dir(data_dir: Path) -> Path:
    return data_dir / "checks" / "dashboard"


def write_launch_evidence(data_dir: Path, launch_payload: dict[str, Any], preflight_status: str = "ok") -> Path:
    evidence = LaunchEvidence(
        timestamp=utc_timestamp(),
        status=str(launch_payload.get("status", "unknown")),
        url=str(launch_payload.get("url", "")),
        port=int(launch_payload.get("port", 0) or 0),
        pid=launch_payload.get("pid") if launch_payload.get("pid") is None else int(launch_payload["pid"]),
        log_path=str(launch_payload.get("log_path", "")),
        error_log_path=str(launch_payload.get("error_log_path", "")),
        live_trading_enabled=False,
        kill_switch=bool(launch_payload.get("kill_switch", True)),
        preflight_status=preflight_status,
    )
    out = dashboard_checks_dir(data_dir) / "launch-evidence.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(redact_payload(evidence.to_dict()), indent=2, default=str), encoding="utf-8")
    return out


def build_operator_evidence(
    settings: BotSettings,
    *,
    mode: str,
    profile: str,
    source: str,
    snapshot: Any | None = None,
    connectivity: dict[str, Any] | None = None,
    runner_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    snapshot_payload = snapshot_to_summary(snapshot)
    runner_payload = runner_status if runner_status is not None else PilotRunnerService(settings).status()
    payload = {
        "timestamp": utc_timestamp(),
        "mode": mode,
        "profile": profile,
        "source": source,
        "base_url": settings.active_base_url,
        "live_trading_enabled": False,
        "kill_switch": True,
        "connectivity": connectivity or {},
        "snapshot": snapshot_payload,
        "runner": {
            "state": runner_payload.get("runner", {}).get("state", "unknown"),
            "alive": runner_payload.get("runner", {}).get("alive", False),
            "stale": runner_payload.get("runner", {}).get("stale", False),
            "heartbeat_age_ms": runner_payload.get("runner", {}).get("heartbeat_age_ms", 0),
            "health": runner_payload.get("runner_health", {}),
            "telemetry_summary": runner_payload.get("telemetry_summary", {}),
            "commands": runner_payload.get("commands", []),
        },
        "dashboard": {
            "pages": [page.key for page in PAGES],
            "page_titles": [page.title for page in PAGES],
            "chart_keys": list(all_chart_keys()),
            "unique_chart_keys": len(all_chart_keys()) == len(set(all_chart_keys())),
        },
        "demo_execution_drill": _latest_demo_execution_drill(settings.data_dir),
    }
    return redact_payload(payload)


def snapshot_to_summary(snapshot: Any | None) -> dict[str, Any]:
    if snapshot is None:
        return {}
    return redact_payload(
        {
            "mode": getattr(snapshot, "mode", ""),
            "symbol": getattr(snapshot, "symbol", ""),
            "interval": getattr(snapshot, "interval", ""),
            "status": getattr(snapshot, "status", ""),
            "message": getattr(snapshot, "message", ""),
            "session_id": getattr(snapshot, "session_id", ""),
            "demo_connection": getattr(snapshot, "demo_connection", {}),
            "readiness": getattr(snapshot, "readiness", {}),
        }
    )


def write_operator_evidence(settings: BotSettings, payload: dict[str, Any]) -> Path:
    out_dir = settings.data_dir / "evidence" / "dashboard"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = utc_timestamp().replace(":", "").replace("+", "Z")
    out = out_dir / f"operator-evidence-{stamp}.json"
    out.write_text(json.dumps(redact_payload(payload), indent=2, default=str), encoding="utf-8")
    return out


def _latest_demo_execution_drill(data_dir: Path) -> dict[str, Any]:
    path = data_dir / "evidence" / "demo-execution" / "demo_execution_drill.json"
    if not path.exists():
        return {"status": "missing", "path": str(path)}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"status": "invalid", "path": str(path)}
