from .model_ops_facade import training_payload
def train_model(rows: int): return training_payload("model_training", rows)
