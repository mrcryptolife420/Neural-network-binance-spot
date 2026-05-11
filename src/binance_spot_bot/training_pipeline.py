from .training_data_gate import training_data_gate
from .model_training import train_model
def run_training_pipeline(rows: int): return {"gate": training_data_gate(rows, True), "training": train_model(rows), "live_trading_enabled": False}
