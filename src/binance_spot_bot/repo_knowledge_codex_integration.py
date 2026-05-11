from .dev_quality_facade import safe_record
def repo_knowledge_codex_prompt(topic: str): return safe_record("repo_knowledge_codex", {"topic": topic})
