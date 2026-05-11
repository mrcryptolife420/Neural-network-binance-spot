from .dev_quality_facade import safe_record
def roadmap_release_integration(roadmaps: list[str]): return safe_record("roadmap_release_integration", {"roadmaps": roadmaps})
