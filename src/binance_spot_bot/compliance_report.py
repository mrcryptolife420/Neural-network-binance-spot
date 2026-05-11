from pathlib import Path
from .permission_profiles import permission_compliance_report
def write_compliance_report(settings): return permission_compliance_report(settings)
