from .local_paper_os_facade import safe_record
def detect_metric_anomalies(rows: list[dict]): return safe_record("metric_anomalies", {"anomalies": [r for r in rows if float(r.get("value", 0)) < 0]})
