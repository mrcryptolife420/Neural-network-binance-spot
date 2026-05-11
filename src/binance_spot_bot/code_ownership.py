from .dev_quality_facade import safe_record
def code_ownership(files: list[str]): return safe_record("code_ownership", {"owners": {file: "local" for file in files}})
