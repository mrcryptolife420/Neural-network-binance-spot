from .model_ops_facade import training_payload
def model_artifacts(model_id: str): return training_payload("model_artifacts", 1) | {"model_id": model_id}
