from .dev_quality_facade import safe_record
def cli_surface_map(commands: list[str]): return safe_record("cli_surface_map", {"commands": commands})
