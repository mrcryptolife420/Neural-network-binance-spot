from .dev_quality_facade import safe_record
def artifact_flow_graph(artifacts: list[str]): return safe_record("artifact_flow_graph", {"artifacts": artifacts, "edges": []})
