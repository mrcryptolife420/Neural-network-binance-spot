from .dev_quality_facade import safe_record
def data_lineage(source: str, target: str): return safe_record("data_lineage", {"source": source, "target": target})
