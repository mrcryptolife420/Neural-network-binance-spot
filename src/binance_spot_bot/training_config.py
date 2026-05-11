from .model_ops_facade import training_payload
def training_config(symbols: list[str]): return training_payload("training_config", len(symbols))
