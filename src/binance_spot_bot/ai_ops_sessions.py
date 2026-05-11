from pathlib import Path
from .local_paper_os_facade import safe_record, write_json_report
def write_ai_ops_session(root: Path, question: str, answer: dict): return write_json_report(root, "ai-ops-sessions", "latest-session", safe_record("ai_ops_session", {"question": question, "answer": answer}))
