from pathlib import Path
from .action_center import write_action_journal
def append_decision(root: Path, decision: dict): return write_action_journal(type("S", (), {"data_dir": root})(), decision)
