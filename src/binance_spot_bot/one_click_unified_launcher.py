from .local_paper_os_facade import safe_record
def one_click_unified_launcher(mode: str = "demo"): return safe_record("one_click_unified_launcher", {"mode": mode, "opens_dashboard": True, "safe_live_gate": True})
