from .model_ops_facade import training_payload
def model_evaluation_pack(score: float): return training_payload("model_evaluation_pack", int(score * 100))
