from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class EvidenceRecord:
    record_id: str
    kind: str
    payload: dict[str, Any]
    sha256: str
    created_at_ms: int

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


class EvidenceVault:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, kind: str, payload: dict[str, Any]) -> EvidenceRecord:
        safe_payload = redact_payload(payload)
        encoded = json.dumps(safe_payload, sort_keys=True, default=str).encode("utf-8")
        record = EvidenceRecord(f"ev-{int(time.time() * 1000)}", kind, safe_payload, hashlib.sha256(encoded).hexdigest(), int(time.time() * 1000))
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record.to_dict(), sort_keys=True, default=str) + "\n")
        return record

    def list(self) -> list[EvidenceRecord]:
        if not self.path.exists():
            return []
        return [EvidenceRecord(**json.loads(line)) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def verify(self, record: EvidenceRecord) -> bool:
        encoded = json.dumps(record.payload, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest() == record.sha256

    def export(self, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps([record.to_dict() for record in self.list()], indent=2, default=str), encoding="utf-8")
        return output_path
