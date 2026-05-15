from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload

NO_LIVE_STATEMENT = "MARKET INTELLIGENCE - NO LIVE TRADING"
PUBLIC_DATA_ONLY_STATEMENT = "PUBLIC UNSIGNED BINANCE SPOT MARKET DATA ONLY"
NO_FINANCIAL_ADVICE_STATEMENT = "SCANNER RANKINGS ARE RESEARCH METRICS, NOT FINANCIAL ADVICE"


def allowed_public_market_methods() -> tuple[str, ...]:
    return (
        "get_exchange_info",
        "get_klines",
        "get_ui_klines",
        "get_order_book",
        "get_24hr_ticker",
        "get_rolling_ticker",
        "get_avg_price",
        "get_recent_trades",
        "get_agg_trades",
        "get_book_ticker",
    )


def forbidden_signed_or_account_methods() -> tuple[str, ...]:
    return (
        "get_account_state",
        "test_order",
        "place_order",
        "cancel_order",
        "get_order",
        "open_orders",
        "query_order",
        "create_listen_key",
        "keepalive_listen_key",
        "close_listen_key",
    )


@dataclass(frozen=True)
class PublicEndpointCheck:
    method_name: str
    status: str
    reason: str
    signed_or_account_endpoint: bool = False
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class PublicEndpointPolicyReport:
    checks: tuple[PublicEndpointCheck, ...]
    no_live_statement: str = NO_LIVE_STATEMENT
    public_data_only_statement: str = PUBLIC_DATA_ONLY_STATEMENT
    no_financial_advice_statement: str = NO_FINANCIAL_ADVICE_STATEMENT
    live_trading_enabled: bool = False
    blockers: tuple[str, ...] = field(default_factory=tuple)

    @property
    def status(self) -> str:
        return "ok" if not self.blockers else "blocked"


@dataclass(frozen=True)
class PublicEndpointPolicy:
    allowed_methods: tuple[str, ...] = field(default_factory=allowed_public_market_methods)
    forbidden_methods: tuple[str, ...] = field(default_factory=forbidden_signed_or_account_methods)
    unknown_methods_blocked: bool = True


def check_market_intelligence_endpoint(method_name: str, policy: PublicEndpointPolicy | None = None) -> PublicEndpointCheck:
    policy = policy or PublicEndpointPolicy()
    if method_name in policy.allowed_methods:
        return PublicEndpointCheck(method_name, "allowed", "public unsigned market data endpoint")
    if method_name in policy.forbidden_methods:
        return PublicEndpointCheck(method_name, "blocked", "signed/account/order endpoint forbidden", signed_or_account_endpoint=True)
    return PublicEndpointCheck(method_name, "blocked" if policy.unknown_methods_blocked else "unknown", "unknown endpoint blocked by default")


def assert_public_market_endpoint(method_name: str) -> None:
    check = check_market_intelligence_endpoint(method_name)
    if check.status != "allowed":
        raise ValueError(f"market intelligence endpoint blocked: {method_name}")


def build_public_endpoint_policy_report(methods: list[str] | tuple[str, ...] | None = None) -> PublicEndpointPolicyReport:
    methods = methods or (*allowed_public_market_methods(), *forbidden_signed_or_account_methods(), "unknown_method")
    checks = tuple(check_market_intelligence_endpoint(method) for method in methods)
    blockers = tuple(f"{check.method_name}: {check.reason}" for check in checks if check.method_name in allowed_public_market_methods() and check.status != "allowed")
    return PublicEndpointPolicyReport(checks=checks, blockers=blockers)


def public_endpoint_policy_report_to_dict(report: PublicEndpointPolicyReport) -> dict[str, Any]:
    payload = asdict(report)
    payload["status"] = report.status
    return redact_payload(payload)


def write_public_endpoint_policy_report(root: Path | str = ".") -> dict[str, Any]:
    out = Path(root) / "data" / "market-intelligence" / "policy"
    out.mkdir(parents=True, exist_ok=True)
    payload = public_endpoint_policy_report_to_dict(build_public_endpoint_policy_report())
    json_path = out / "public-endpoint-policy.json"
    md_path = out / "public-endpoint-policy.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(f"# Public Endpoint Policy\n\nStatus: {payload['status']}\n\n{NO_FINANCIAL_ADVICE_STATEMENT}\n", encoding="utf-8")
    return {"status": payload["status"], "json": str(json_path), "markdown": str(md_path), "report": payload, "live_trading_enabled": False}
