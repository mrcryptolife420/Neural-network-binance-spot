from __future__ import annotations

import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from binance_spot_bot.backup_restore import create_backup, restore_backup
from binance_spot_bot.config import BotSettings
from binance_spot_bot.diagnostics import collect_diagnostics
from binance_spot_bot.support_bundle import create_support_bundle
from binance_spot_bot.workspaces import WorkspaceProfile, WorkspaceStore


class WorkspaceBackupDiagnosticsTests(unittest.TestCase):
    def settings(self, tmp: str) -> BotSettings:
        env = {
            "DATA_DIR": str(Path(tmp) / "data"),
            "AUDIT_LOG_PATH": str(Path(tmp) / "data" / "audit" / "events.jsonl"),
        }
        with patch.dict(os.environ, env, clear=True):
            return BotSettings.from_env()

    def test_workspace_profile_roundtrip_without_secrets(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = WorkspaceStore(Path(tmp) / "workspaces")
            store.save(WorkspaceProfile("Demo", "data/demo", "local-demo", ["BTCUSDT"], risk_preset="safe"))
            loaded = store.load("Demo")
        self.assertEqual(loaded.symbols, ["BTCUSDT"])
        self.assertEqual(loaded.exchange_profile, "local-demo")

    def test_backup_redacts_and_restore_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "data"
            root.mkdir()
            (root / "settings.json").write_text('{"api_secret":"abcdefghijklmnopqrstuvwxyz"}', encoding="utf-8")
            backup = Path(tmp) / "backup.zip"
            manifest = create_backup([root], backup)
            self.assertIn("data/settings.json", manifest.files)
            with zipfile.ZipFile(backup, "r") as archive:
                payload = archive.read("data/settings.json").decode("utf-8")
            self.assertIn("[REDACTED]", payload)
            with self.assertRaises(ValueError):
                restore_backup(backup, Path(tmp) / "restore")

    def test_diagnostics_and_support_bundle_are_redacted_zip_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = self.settings(tmp)
            diagnostics = collect_diagnostics(settings).to_dict()
            bundle = create_support_bundle(settings, Path(tmp) / "support.zip")
            with zipfile.ZipFile(bundle["bundle"], "r") as archive:
                names = set(archive.namelist())
        self.assertFalse(diagnostics["live_trading_enabled"])
        self.assertIn("manifest.json", names)
        self.assertIn("preflight.json", names)


if __name__ == "__main__":
    unittest.main()
