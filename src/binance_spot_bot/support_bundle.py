from __future__ import annotations

import hashlib
import json
import zipfile
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from .config import BotSettings
from .diagnostics import OperatorDiagnostics
from .preflight import run_preflight
from .redaction import redact_payload, redact_text


def create_support_bundle(settings: BotSettings, output_zip: Path) -> dict[str, Any]:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    diagnostics = OperatorDiagnostics(settings)
    diagnostics_payload = diagnostics.state_health().to_dict()
    preflight_payload = run_preflight(settings, include_security_scan=False).to_dict()
    files: list[dict[str, Any]] = []

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        _write_json(archive, "diagnostics.json", diagnostics_payload, files)
        _write_json(archive, "preflight.json", preflight_payload, files)
        _write_json(archive, "settings-redacted.json", _settings_payload(settings), files)
        for item in diagnostics_payload.get("artifact_inventory", []):
            if not item.get("exists"):
                continue
            source = Path(str(item.get("path", "")))
            if source.is_file() and _allowed_artifact(settings, source):
                _write_file(archive, source, f"artifacts/{item.get('name')}.json", files)
        manifest = {
            "files": files,
            "redaction": "all payloads passed through redact_payload/redact_text",
            "live_trading_enabled": False,
        }
        archive.writestr("manifest.json", json.dumps(manifest, indent=2, default=str))

    return redact_payload({"bundle": str(output_zip), "manifest": "manifest.json", "files": len(files), "live_trading_enabled": False})


def verify_support_bundle(bundle_zip: Path) -> dict[str, Any]:
    if not bundle_zip.exists():
        return {"status": "fail", "bundle": str(bundle_zip), "errors": ["bundle missing"], "live_trading_enabled": False}
    errors: list[str] = []
    with zipfile.ZipFile(bundle_zip, "r") as archive:
        names = set(archive.namelist())
        if "manifest.json" not in names:
            return {"status": "fail", "bundle": str(bundle_zip), "errors": ["manifest missing"], "live_trading_enabled": False}
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
        for item in manifest.get("files", []):
            name = str(item.get("path", ""))
            if name not in names:
                errors.append(f"missing file: {name}")
                continue
            digest = hashlib.sha256(archive.read(name)).hexdigest()
            if _format_sha256(digest) != item.get("sha256"):
                errors.append(f"checksum mismatch: {name}")
    return redact_payload(
        {
            "status": "fail" if errors else "ok",
            "bundle": str(bundle_zip),
            "errors": errors,
            "files": len(manifest.get("files", [])),
            "live_trading_enabled": False,
        }
    )


def _write_json(archive: zipfile.ZipFile, name: str, payload: Any, files: list[dict[str, Any]]) -> None:
    data = json.dumps(redact_payload(payload), indent=2, default=str).encode("utf-8")
    archive.writestr(name, data)
    files.append(_manifest_entry(name, data))


def _write_file(archive: zipfile.ZipFile, source: Path, name: str, files: list[dict[str, Any]]) -> None:
    text = redact_text(source.read_text(encoding="utf-8", errors="replace"))
    data = text.encode("utf-8")
    archive.writestr(name, data)
    files.append(_manifest_entry(name, data))


def _manifest_entry(name: str, data: bytes) -> dict[str, Any]:
    return {"path": name, "size_bytes": len(data), "sha256": _format_sha256(hashlib.sha256(data).hexdigest()), "redacted": True}


def _format_sha256(digest: str) -> str:
    return "-".join(digest[index : index + 8] for index in range(0, len(digest), 8))


def _settings_payload(settings: BotSettings) -> dict[str, Any]:
    if is_dataclass(settings):
        return redact_payload(asdict(settings))
    return redact_payload(dict(settings.__dict__))


def _allowed_artifact(settings: BotSettings, source: Path) -> bool:
    try:
        source.resolve().relative_to(Path(settings.data_dir).resolve())
    except ValueError:
        return False
    lowered = source.name.lower()
    if lowered in {".env"} or lowered.endswith((".pem", ".key")):
        return False
    return True
