from .local_paper_os_facade import safe_record
def search_ai_ops_index(query: str, docs: list[str]): return safe_record("ai_ops_index", {"matches": [doc for doc in docs if query.lower() in doc.lower()]})
