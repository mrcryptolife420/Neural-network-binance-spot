from .model_ops_facade import training_payload
def model_alias_history(alias: str): return training_payload("model_alias_history", 1) | {"alias": alias}
