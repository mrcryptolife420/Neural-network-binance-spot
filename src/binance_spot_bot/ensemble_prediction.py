from .model_ops_facade import ensemble_vote
def ensemble_prediction(predictions: list[dict]): return ensemble_vote(predictions)
