from .model_ops_facade import training_payload
def experiment_tracker(rows: int = 0): return training_payload("experiment_tracker", rows)
