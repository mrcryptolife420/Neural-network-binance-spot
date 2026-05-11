from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PageDefinition:
    key: str
    title: str
    live_trading_enabled: bool = False


PAGES: tuple[PageDefinition, ...] = (
    PageDefinition("overview", "Overview"),
    PageDefinition("demo_spot_trading", "Demo Spot Trading"),
    PageDefinition("credentials_profile", "Credentials & Profile"),
    PageDefinition("bot_controls", "Bot Controls"),
    PageDefinition("risk_controls", "Risk Controls"),
    PageDefinition("strategy_model", "Strategy & Model"),
    PageDefinition("market_data", "Market Data"),
    PageDefinition("orders_account", "Orders & Account"),
    PageDefinition("sessions", "Sessions"),
    PageDefinition("evaluation", "Evaluation"),
    PageDefinition("strategy_lab", "Strategy Lab"),
    PageDefinition("research", "Research"),
    PageDefinition("portfolio", "Portfolio"),
    PageDefinition("readiness", "Readiness"),
    PageDefinition("logs_security", "Logs & Security"),
    PageDefinition("demo_pilot", "Demo Pilot"),
    PageDefinition("policy_governance", "Policy Governance"),
    PageDefinition("ops_automation", "Ops Automation"),
    PageDefinition("observability", "Observability"),
    PageDefinition("ai_ops_assistant", "AI Ops Assistant"),
    PageDefinition("action_center", "Action Center"),
    PageDefinition("permissions", "Permissions"),
    PageDefinition("disaster_recovery", "Disaster Recovery"),
    PageDefinition("release_management", "Release Management"),
    PageDefinition("roadmap_automation", "Roadmap Automation"),
    PageDefinition("repo_knowledge", "Repo Knowledge"),
    PageDefinition("test_selection", "Test Selection"),
    PageDefinition("performance", "Performance"),
    PageDefinition("runtime_core", "Runtime Core"),
    PageDefinition("data_pipeline", "Data Pipeline"),
    PageDefinition("model_training", "Model Training"),
    PageDefinition("model_monitoring", "Model Monitoring"),
    PageDefinition("portfolio_ensemble", "Portfolio Ensemble"),
    PageDefinition("paper_os_audit", "Paper OS Audit"),
    PageDefinition("stabilization", "Stabilization"),
    PageDefinition("operator_training", "Operator Training"),
)


def page_titles() -> list[str]:
    return [page.title for page in PAGES]


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
