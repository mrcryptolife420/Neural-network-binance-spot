from .dev_quality_facade import data_contract
def feature_schema(columns: list[str]): return data_contract("|".join(columns), len(columns))
