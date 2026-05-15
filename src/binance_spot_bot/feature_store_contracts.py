from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .dataset_governance import feature_schema_from_rows
from .types import FeatureRow


@dataclass(frozen=True)
class FeatureStoreContract:
    dataset_id: str
    schema_hash: str
    feature_names: list[str]
    generator_version: str
    lookback_window: int
    live_trading_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def contract_from_features(dataset_id: str, rows: list[FeatureRow], lookback_window: int) -> FeatureStoreContract:
    schema = feature_schema_from_rows(rows, lookback_window=lookback_window)
    return FeatureStoreContract(dataset_id, schema.schema_hash, schema.feature_names, schema.generator_version, lookback_window)


def validate_feature_contract(rows: list[FeatureRow], contract: FeatureStoreContract) -> dict[str, Any]:
    actual = contract_from_features(contract.dataset_id, rows, contract.lookback_window)
    status = "ok" if actual.schema_hash == contract.schema_hash else "failed"
    return {"status": status, "expected": contract.to_dict(), "actual": actual.to_dict(), "live_trading_enabled": False}
