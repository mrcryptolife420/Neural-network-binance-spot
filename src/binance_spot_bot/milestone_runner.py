from .model_ops_facade import training_payload
def milestone_runner(name: str): return training_payload("milestone_runner", 1) | {"name": name}
