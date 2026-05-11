from .model_ops_facade import training_payload
def ensemble_config(models: list[str]): return training_payload("ensemble_config", len(models)) | {"models": models}
