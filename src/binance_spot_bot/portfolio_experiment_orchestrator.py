from .local_paper_os_facade import safe_record
def portfolio_experiment_orchestrator(basket: list[str]): return safe_record("portfolio_experiment_orchestrator", {"basket": basket, "simulation_only": True})
