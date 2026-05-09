from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class WizardOption:
    key: str
    label: str
    requires_keys: bool
    mode: str
    source: str
    description: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


WIZARD_OPTIONS = (
    WizardOption("local-demo", "Local demo replay", False, "demo", "demo", "Safest first start; no internet or keys."),
    WizardOption("paper-public-spot", "Binance public Spot paper", False, "paper", "rest", "Uses public market data and paper fills."),
    WizardOption("binance-demo-spot-readiness", "Binance Demo Spot API", True, "testnet-readiness", "rest", "Checks demo credentials without live trading."),
    WizardOption("binance-spot-testnet-readiness", "Spot Testnet readiness", True, "testnet-readiness", "rest", "Checks testnet setup without live trading."),
)


def wizard_options() -> list[dict[str, object]]:
    return [item.to_dict() for item in WIZARD_OPTIONS]


def option_for(key: str) -> WizardOption:
    for item in WIZARD_OPTIONS:
        if item.key == key:
            return item
    raise ValueError(f"unsupported wizard option: {key}")
