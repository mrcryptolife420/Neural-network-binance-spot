from __future__ import annotations

import importlib.metadata
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .config import BotSettings
from .redaction import redact_payload


@dataclass(frozen=True)
class DiagnosticsReport:
    python: str
    platform: str
    data_dir: str
    audit_log_path: str
    packages: dict[str, str]
    live_trading_enabled: bool

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def collect_diagnostics(settings: BotSettings) -> DiagnosticsReport:
    packages = {}
    for package in ("streamlit", "plotly"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "missing"
    return DiagnosticsReport(
        python=sys.version.split()[0],
        platform=platform.platform(),
        data_dir=str(Path(settings.data_dir)),
        audit_log_path=str(Path(settings.audit_log_path)),
        packages=packages,
        live_trading_enabled=settings.live_trading_enabled,
    )
