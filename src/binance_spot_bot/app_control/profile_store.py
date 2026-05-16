from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .bot_profile import BotProfile, bot_profile_to_dict, built_in_profiles, validate_bot_profile
from binance_spot_bot.portfolio_lab.common import json_write, path_in


class ProfileStore:
    def __init__(self, root: Path) -> None:
        self.root = path_in(root, "data", "app-control", "profiles")
        self.user = path_in(self.root, "user")
        self.user.mkdir(parents=True, exist_ok=True)

    def templates(self) -> dict[str, Any]:
        profiles = [bot_profile_to_dict(profile) for profile in built_in_profiles()]
        return {"status": "ok", "profiles": profiles, "live_trading_enabled": False}

    def save(self, profile: BotProfile) -> dict[str, Any]:
        validation = validate_bot_profile(profile)
        if validation.status == "blocked":
            return {"status": "blocked", "validation": validation.__dict__, "live_trading_enabled": False}
        return json_write(self.user / f"{profile.profile_id}.json", {"profile": bot_profile_to_dict(profile), "validation": validation.__dict__, "live_trading_enabled": False})

    def list(self) -> dict[str, Any]:
        rows = self.templates()["profiles"]
        for path in sorted(self.user.glob("*.json")):
            rows.append(json.loads(path.read_text(encoding="utf-8")).get("profile", {}))
        return {"status": "ok", "profiles": rows, "live_trading_enabled": False}

    def validate_all(self) -> dict[str, Any]:
        rows = [{"profile_id": profile.profile_id, "validation": validate_bot_profile(profile).__dict__} for profile in built_in_profiles()]
        return {"status": "ok" if all(row["validation"]["status"] == "ok" for row in rows) else "blocked", "validations": rows, "live_trading_enabled": False}


def default_profile_store(root: Path) -> ProfileStore:
    return ProfileStore(root)

