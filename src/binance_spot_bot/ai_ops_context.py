from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .ai_ops_injection_guard import injection_guard
from .redaction import redact_payload, redact_text


@dataclass(frozen=True)
class AiOpsContextSource:
    name: str
    path: str
    status: str
    timestamp_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    sha256: str = ""
    redacted: bool = True


@dataclass(frozen=True)
class AiOpsContextItem:
    source: str
    content: dict[str, Any] | str
    suspicious: bool = False


@dataclass(frozen=True)
class AiOpsContextManifest:
    sources: list[AiOpsContextSource]
    warnings: list[str]
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class AiOpsContextPack:
    items: list[AiOpsContextItem]
    manifest: AiOpsContextManifest
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


@dataclass(frozen=True)
class AiOpsContextBuildResult:
    status: str
    context: AiOpsContextPack
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


DEFAULT_CONTEXT_FILES = [
    ("dashboard_smoke", "checks/dashboard/browser-smoke.json"),
    ("metrics_manifest", "metrics-warehouse/manifests/metrics-manifest.json"),
    ("governance_reminders", "local-ops/reports/governance_reminders.json"),
    ("report_index", "reports/report-index.json"),
    ("support_bundle", "support/manifest.json"),
]


def build_ai_ops_context(root: Path, *, max_chars_per_source: int = 4000) -> dict[str, Any]:
    root = Path(root)
    items: list[AiOpsContextItem] = []
    sources: list[AiOpsContextSource] = []
    warnings: list[str] = []
    for name, rel in DEFAULT_CONTEXT_FILES:
        path = root / rel
        if not path.exists():
            warnings.append(f"missing:{name}")
            sources.append(AiOpsContextSource(name, rel, "missing"))
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")[:max_chars_per_source]
        guarded = injection_guard(raw)
        content = _json_or_text(guarded["safe_text"])
        digest = hashlib.sha256(guarded["safe_text"].encode("utf-8")).hexdigest()
        digest_short = f"{digest[:16]}...{digest[-16:]}"
        sources.append(AiOpsContextSource(name, rel, guarded["status"], sha256=digest_short))
        items.append(AiOpsContextItem(name, content, suspicious=guarded["suspicious"]))
        if guarded["suspicious"]:
            warnings.append(f"suspicious:{name}")
    pack = AiOpsContextPack(items, AiOpsContextManifest(sources, warnings))
    return AiOpsContextBuildResult("ready" if items else "partial", pack).to_dict()


def write_ai_ops_context(root: Path, context: dict[str, Any]) -> Path:
    out = root / "ai-ops" / "contexts"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "latest-context.json"
    path.write_text(json.dumps(redact_payload(context), indent=2, default=str), encoding="utf-8")
    return path


def _json_or_text(value: str) -> dict[str, Any] | str:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return redact_text(value)
    return redact_payload(parsed)
