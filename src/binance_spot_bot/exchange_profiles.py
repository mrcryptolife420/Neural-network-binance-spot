from __future__ import annotations

from dataclasses import asdict, dataclass

from .types import TradingMode


LOCAL_DEMO_PROFILE = "local-demo"
BINANCE_DEMO_SPOT_PROFILE = "binance-demo-spot"
BINANCE_SPOT_TESTNET_PROFILE = "binance-spot-testnet"


@dataclass(frozen=True)
class CredentialProfile:
    name: str
    label: str
    mode_badge: str
    trading_mode: TradingMode
    rest_base_url: str
    websocket_base_url: str
    user_data_stream_enabled: bool
    requires_credentials: bool
    storage: str = "session"

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["trading_mode"] = self.trading_mode.value
        return payload


def profile_for(name: str) -> CredentialProfile:
    profiles = available_profiles()
    if name not in profiles:
        raise ValueError(f"unsupported exchange profile: {name}")
    return profiles[name]


def available_profiles() -> dict[str, CredentialProfile]:
    return {
        LOCAL_DEMO_PROFILE: CredentialProfile(
            name=LOCAL_DEMO_PROFILE,
            label="Local demo replay",
            mode_badge="LOCAL DEMO",
            trading_mode=TradingMode.DISABLED,
            rest_base_url="local-demo",
            websocket_base_url="local-demo",
            user_data_stream_enabled=False,
            requires_credentials=False,
        ),
        BINANCE_DEMO_SPOT_PROFILE: CredentialProfile(
            name=BINANCE_DEMO_SPOT_PROFILE,
            label="Binance Demo Spot API",
            mode_badge="BINANCE DEMO SPOT",
            trading_mode=TradingMode.TESTNET,
            rest_base_url="https://demo-api.binance.com",
            websocket_base_url="wss://stream.binance.com:9443",
            user_data_stream_enabled=True,
            requires_credentials=True,
        ),
        BINANCE_SPOT_TESTNET_PROFILE: CredentialProfile(
            name=BINANCE_SPOT_TESTNET_PROFILE,
            label="Binance Spot Testnet",
            mode_badge="BINANCE SPOT TESTNET",
            trading_mode=TradingMode.TESTNET,
            rest_base_url="https://testnet.binance.vision",
            websocket_base_url="wss://stream.testnet.binance.vision",
            user_data_stream_enabled=True,
            requires_credentials=True,
        ),
    }


def selectable_profile_names() -> tuple[str, ...]:
    return tuple(available_profiles().keys())
