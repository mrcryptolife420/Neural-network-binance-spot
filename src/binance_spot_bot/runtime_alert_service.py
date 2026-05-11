from .dev_quality_facade import runtime_event
def runtime_alert_service(alerts: list[dict]): return runtime_event("alert_service", {"alerts": alerts})
