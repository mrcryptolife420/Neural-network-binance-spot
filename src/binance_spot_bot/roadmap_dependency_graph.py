from .dev_quality_facade import safe_record
def roadmap_dependency_graph(names: list[str]): return safe_record("roadmap_dependency_graph", {"nodes": names, "edges": []})
