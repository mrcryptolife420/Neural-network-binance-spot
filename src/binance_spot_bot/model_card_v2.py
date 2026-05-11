from .model_ops_facade import training_payload
def model_card_v2(model_id: str): return training_payload("model_card_v2", 1) | {"model_id": model_id}
