from __future__ import annotations

import json
import zipfile
from pathlib import Path

from .config import BotSettings
from .diagnostics import collect_diagnostics
from .preflight import run_preflight


def create_support_bundle(settings: BotSettings, output_zip: Path) -> dict[str, str]:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    diagnostics = collect_diagnostics(settings).to_dict()
    preflight = run_preflight(settings, include_security_scan=False).to_dict()
    manifest = {"diagnostics": "diagnostics.json", "preflight": "preflight.json"}
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("diagnostics.json", json.dumps(diagnostics, indent=2, default=str))
        archive.writestr("preflight.json", json.dumps(preflight, indent=2, default=str))
        archive.writestr("manifest.json", json.dumps(manifest, indent=2))
    return {"bundle": str(output_zip), "manifest": "manifest.json"}
