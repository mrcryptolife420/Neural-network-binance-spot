from __future__ import annotations

import json
import zipfile
from dataclasses import replace
from pathlib import Path

from binance_spot_bot.config import BotSettings
from binance_spot_bot.support_bundle import create_support_bundle


def settings(tmp_path: Path) -> BotSettings:
    return replace(BotSettings.from_env(), data_dir=tmp_path / "data", audit_log_path=tmp_path / "data" / "audit" / "events.jsonl")


def test_support_bundle_manifest_checksums_and_redaction(tmp_path: Path) -> None:
    s = settings(tmp_path)
    secret = "abcde" * 8
    artifact = s.data_dir / "checks" / "dashboard" / "launch-evidence.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps({"api_secret": secret, "live_trading_enabled": False}), encoding="utf-8")

    result = create_support_bundle(s, tmp_path / "support.zip")
    with zipfile.ZipFile(result["bundle"], "r") as archive:
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
        combined = "\n".join(archive.read(name).decode("utf-8", errors="replace") for name in archive.namelist())

    assert manifest["files"]
    assert all(row["sha256"] for row in manifest["files"])
    assert secret not in combined
    assert "[REDACTED]" in combined
