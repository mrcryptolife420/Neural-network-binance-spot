from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .backup_profiles import is_forbidden_backup_path
from .redaction import redact_payload


def state_integrity_check(root: Path) -> dict[str, Any]:
    issues = []
    repair_plan = []
    for path in sorted(Path(root).rglob("*")) if Path(root).exists() else []:
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if is_forbidden_backup_path(rel):
            issues.append({"severity": "blocked", "path": rel, "reason": "forbidden_file_present"})
            repair_plan.append({"action": "manual_review_required", "path": rel})
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                issues.append({"severity": "warn", "path": rel, "reason": "invalid_json"})
                repair_plan.append({"action": "quarantine_corrupt_file", "path": rel, "confirm_required": True})
        if path.suffix.lower() == ".jsonl":
            for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    json.loads(line)
                except Exception:
                    issues.append({"severity": "warn", "path": rel, "line": line_no, "reason": "invalid_jsonl"})
                    break
    status = "blocked" if any(item["severity"] == "blocked" for item in issues) else ("warn" if issues else "ok")
    return redact_payload({"status": status, "issues": issues, "repair_plan": repair_plan, "read_only": True, "live_trading_enabled": False})
