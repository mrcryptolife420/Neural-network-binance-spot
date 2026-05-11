from .model_ops_facade import drift_score
def prediction_drift(current: list[float], baseline: list[float]): return drift_score(current, baseline)
