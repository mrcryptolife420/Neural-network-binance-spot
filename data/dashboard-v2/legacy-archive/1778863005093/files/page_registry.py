from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any, Callable


@dataclass(frozen=True)
class PageDefinition:
    key: str
    title: str
    module: str = ""
    render_name: str = "render_page"
    lazy: bool = True
    smoke_required: bool = False
    performance_budget_ms: float = 750.0
    max_rows: int = 250
    live_trading_enabled: bool = False

    def load_renderer(self) -> Callable[..., Any]:
        if not self.module:
            raise ValueError(f"page has no module: {self.key}")
        module = import_module(self.module)
        renderer = getattr(module, self.render_name)
        if not callable(renderer):
            raise TypeError(f"page renderer is not callable: {self.key}.{self.render_name}")
        return renderer


_DEDICATED_PAGE_MODULES = {"overview", "demo_spot_trading", "demo_pilot", "performance"}


def _page(key: str, title: str, *, smoke_required: bool = False, budget_ms: float = 750.0) -> PageDefinition:
    module = f"binance_spot_bot.ui.pages.{key}" if key in _DEDICATED_PAGE_MODULES else "binance_spot_bot.ui.pages"
    return PageDefinition(
        key=key,
        title=title,
        module=module,
        smoke_required=smoke_required,
        performance_budget_ms=budget_ms,
    )


PAGES: tuple[PageDefinition, ...] = (
    _page("overview", "Overview", smoke_required=True, budget_ms=500.0),
    _page("demo_spot_trading", "Demo Spot Trading", smoke_required=True, budget_ms=700.0),
    _page("credentials_profile", "Credentials & Profile"),
    _page("bot_controls", "Bot Controls"),
    _page("risk_controls", "Risk Controls"),
    _page("strategy_model", "Strategy & Model"),
    _page("market_data", "Market Data"),
    _page("orders_account", "Orders & Account"),
    _page("sessions", "Sessions"),
    _page("evaluation", "Evaluation"),
    _page("strategy_lab", "Strategy Lab"),
    _page("research", "Research"),
    _page("portfolio", "Portfolio"),
    _page("readiness", "Readiness"),
    _page("logs_security", "Logs & Security"),
    _page("demo_pilot", "Demo Pilot", smoke_required=True, budget_ms=700.0),
    _page("policy_governance", "Policy Governance"),
    _page("ops_automation", "Ops Automation"),
    _page("observability", "Observability"),
    _page("ai_ops_assistant", "AI Ops Assistant"),
    _page("action_center", "Action Center"),
    _page("permissions", "Permissions"),
    _page("disaster_recovery", "Disaster Recovery"),
    _page("release_management", "Release Management"),
    _page("roadmap_automation", "Roadmap Automation"),
    _page("repo_knowledge", "Repo Knowledge"),
    _page("test_selection", "Test Selection"),
    _page("performance", "Performance", smoke_required=True, budget_ms=650.0),
    _page("runtime_core", "Runtime Core"),
    _page("data_pipeline", "Data Pipeline"),
    _page("model_training", "Model Training"),
    _page("model_monitoring", "Model Monitoring"),
    _page("portfolio_ensemble", "Portfolio Ensemble"),
    _page("paper_os_audit", "Paper OS Audit"),
    _page("stabilization", "Stabilization"),
    _page("operator_training", "Operator Training"),
)


def page_titles() -> list[str]:
    return [page.title for page in PAGES]


def page_by_key(key: str) -> PageDefinition:
    for page in PAGES:
        if page.key == key:
            return page
    raise KeyError(key)


def dashboard_page_contract() -> dict[str, object]:
    validate_page_registry()
    return {
        "status": "ok",
        "page_count": len(PAGES),
        "lazy_sections": all(page.lazy for page in PAGES),
        "smoke_pages": [page.key for page in PAGES if page.smoke_required],
        "budget_ms": {page.key: page.performance_budget_ms for page in PAGES},
        "live_trading_enabled": False,
    }


def validate_page_registry() -> None:
    keys = [page.key for page in PAGES]
    titles = [page.title for page in PAGES]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate dashboard page key")
    if len(titles) != len(set(titles)):
        raise ValueError("Duplicate dashboard page title")
    live_pages = [page.key for page in PAGES if page.live_trading_enabled]
    if live_pages:
        raise ValueError(f"Live trading pages are not allowed: {live_pages}")
    bad_budgets = [page.key for page in PAGES if page.performance_budget_ms <= 0]
    if bad_budgets:
        raise ValueError(f"Dashboard page budgets must be positive: {bad_budgets}")
    missing_modules = [
        page.key
        for page in PAGES
        if page.module != "binance_spot_bot.ui.pages" and not page.module.startswith("binance_spot_bot.ui.pages.")
    ]
    if missing_modules:
        raise ValueError(f"Dashboard pages must declare lazy page modules: {missing_modules}")
