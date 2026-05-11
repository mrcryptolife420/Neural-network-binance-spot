from .local_paper_os_facade import safe_record
def paper_performance_summary(rows: list[dict]): return safe_record("paper_performance", {"observations": len(rows), "pnl": sum(float(r.get("pnl", 0)) for r in rows)})
