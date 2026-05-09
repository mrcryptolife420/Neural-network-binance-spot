from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import BotSettings
from .exchange_profiles import CredentialProfile, profile_for
from .redaction import fingerprint
from .types import TradingMode


@dataclass(frozen=True)
class CredentialStatus:
    profile: str
    storage: str
    has_api_key: bool
    has_api_secret: bool
    api_key_fingerprint: str
    capability: str

    def to_dict(self) -> dict[str, object]:
        return {
            "profile": self.profile,
            "storage": self.storage,
            "has_api_key": self.has_api_key,
            "has_api_secret": self.has_api_secret,
            "api_key_fingerprint": self.api_key_fingerprint,
            "capability": self.capability,
        }


class CredentialManager:
    def __init__(self) -> None:
        self._api_key = ""
        self._api_secret = ""
        self._profile_name = "local-demo"
        self._storage = "session"

    def set_session_credentials(self, profile_name: str, api_key: str, api_secret: str) -> CredentialStatus:
        profile_for(profile_name)
        self._profile_name = profile_name
        self._api_key = api_key.strip()
        self._api_secret = api_secret.strip()
        self._storage = "session"
        return self.status()

    def clear(self) -> None:
        self._api_key = ""
        self._api_secret = ""
        self._storage = "session"

    def status(self) -> CredentialStatus:
        profile = profile_for(self._profile_name)
        has_pair = bool(self._api_key and self._api_secret)
        if not profile.requires_credentials:
            capability = "No signed credentials required"
        elif has_pair:
            capability = "Credentials loaded for signed checks"
        else:
            capability = "needs credentials"
        return CredentialStatus(
            profile=self._profile_name,
            storage=self._storage,
            has_api_key=bool(self._api_key),
            has_api_secret=bool(self._api_secret),
            api_key_fingerprint=fingerprint(self._api_key),
            capability=capability,
        )

    def apply_to_settings(self, settings: BotSettings, profile_name: str | None = None) -> BotSettings:
        from dataclasses import replace

        name = profile_name or self._profile_name
        profile = profile_for(name)
        mode = profile.trading_mode if profile.requires_credentials else TradingMode.DISABLED
        return replace(
            settings,
            exchange_profile=name,
            trading_mode=mode,
            binance_api_key=self._api_key,
            binance_api_secret=self._api_secret,
            binance_testnet_base_url=profile.rest_base_url,
            live_trading_enabled=False,
            kill_switch=True,
        )


class WindowsSecretStoreAdapter:
    def __init__(self, namespace: str = "NeuralNetworkBinanceSpot"):
        self.namespace = namespace

    def is_available(self) -> bool:
        script = "Get-Command Get-Secret -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name"
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0 and "Get-Secret" in result.stdout

    def secret_names(self, profile_name: str) -> tuple[str, str]:
        return (f"{self.namespace}:{profile_name}:api-key", f"{self.namespace}:{profile_name}:api-secret")

    def docs_hint(self) -> str:
        return "Install Microsoft.PowerShell.SecretManagement and SecretStore to enable encrypted user-scoped persistence."
