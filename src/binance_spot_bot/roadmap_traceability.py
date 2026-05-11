from .dev_quality_facade import safe_record
def roadmap_traceability(roadmap: str, files: list[str]): return safe_record("roadmap_traceability", {"roadmap": roadmap, "files": files})
