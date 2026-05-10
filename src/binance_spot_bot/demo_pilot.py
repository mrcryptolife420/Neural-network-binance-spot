from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Any

from .binance import BinanceAPIError, BinanceSpotAdapter
from .order_lifecycle import OrderLifecycleStore, TERMINAL_STATUSES
from .redaction import redact_payload


@dataclass(frozen=True)
class DemoPilotConfig:
    pilot_name: str
    duration_minutes: int
    max_demo_orders: int
    max_rejects: int
    max_api_errors: int
    max_reconciliation_failures: int
    cancel_open_orders_on_stop: bool
    reconciliation_interval_seconds: int
    account_sync_interval_seconds: int
    pause_on_connection_degraded: bool = True
    require_clean_start: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DemoPilotCounters:
    orders: int = 0
    rejects: int = 0
    api_errors: int = 0
    reconciliation_failures: int = 0
    started_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))

    def elapsed_seconds(self, now_ms: int | None = None) -> int:
        now_ms = now_ms or int(time.time() * 1000)
        return max(0, (now_ms - self.started_at_ms) // 1000)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["elapsed_seconds"] = self.elapsed_seconds()
        return payload


@dataclass(frozen=True)
class ReconciliationResult:
    status: str
    known_orders: int
    open_orders: int
    orphan_orders: int
    failures: int
    events: list[dict[str, Any]] = field(default_factory=list)
    checked_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))

    @property
    def needs_operator_action(self) -> bool:
        return self.orphan_orders > 0 or self.failures > 0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["needs_operator_action"] = self.needs_operator_action
        return redact_payload(payload)


@dataclass(frozen=True)
class DemoAccountSnapshot:
    status: str
    can_trade: bool | None
    account_type: str
    balances: list[dict[str, Any]]
    last_sync_ms: int
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return redact_payload(asdict(self))


def pilot_presets() -> dict[str, DemoPilotConfig]:
    return {
        "smoke": DemoPilotConfig("smoke", 15, 5, 2, 3, 1, True, 30, 60),
        "operator": DemoPilotConfig("operator", 60, 25, 5, 5, 2, True, 30, 60),
        "endurance": DemoPilotConfig("endurance", 240, 75, 10, 10, 3, True, 60, 120),
    }


def pilot_config(name: str) -> DemoPilotConfig:
    presets = pilot_presets()
    if name not in presets:
        raise ValueError(f"unsupported demo pilot preset: {name}")
    return presets[name]


def operator_checklist(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    connection = snapshot.get("demo_connection", {}) or {}
    account = snapshot.get("demo_account", {}) or {}
    credentials = snapshot.get("credential_status", {}) or {}
    reconciliation = snapshot.get("reconciliation", {}) or {}
    prechecks = snapshot.get("testnet_prechecks", {}) or {}
    pilot = snapshot.get("demo_pilot", {}) or {}
    profile = snapshot.get("exchange_profile", {}) or {}
    gate = connection.get("gate", {}) or {}
    gate_checks = gate.get("checks", {}) or {}

    profile_name = str(profile.get("name") or connection.get("profile") or credentials.get("profile") or "")
    credential_pair = bool(credentials.get("has_api_key") and credentials.get("has_api_secret"))
    connected = bool(connection.get("connected") or connection.get("authenticated"))
    server_time_ok = bool(gate_checks.get("demo_base_url") or connected)
    account_ok = account.get("status") == "ok" and account.get("can_trade") is True
    clean_start_ok = not bool(snapshot.get("resume_required")) and not bool(reconciliation.get("needs_operator_action"))
    orphan_orders = int(reconciliation.get("orphan_orders") or 0)
    risk_limits_set = bool(
        prechecks.get(
            "risk_limits_set",
            all(bool(prechecks.get(name, False)) for name in ("max_daily_loss", "max_position", "max_trades")),
        )
    )
    preset_name = (pilot.get("config", {}) or {}).get("pilot_name", "")
    armed = bool(connection.get("armed"))

    return [
        _check_row("Profile", profile_name == "binance-demo-spot", profile_name or "unknown", True),
        _check_row("Credentials", credential_pair, credentials.get("capability", "not loaded"), True),
        _check_row("Connection", connected, gate.get("reason", "not tested"), True),
        _check_row("Server time", server_time_ok, "demo base URL/gate reachable" if server_time_ok else "test connection first", False),
        _check_row("Account canTrade", account_ok, account.get("error") or account.get("status", "not synced"), True),
        _check_row("Clean start", clean_start_ok, reconciliation.get("status", "not-run"), True),
        _check_row("No orphan orders", orphan_orders == 0, f"{orphan_orders} orphan orders", True),
        _check_row("Risk limits", risk_limits_set, "configured" if risk_limits_set else "missing limits", True),
        _check_row("Pilot preset", bool(preset_name), preset_name or "not selected", False),
        _check_row("Armed", armed, "armed" if armed else "explicit arm required", False),
    ]


def pipeline_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    signal = snapshot.get("latest_signal") or {}
    risk = snapshot.get("latest_risk_decision") or {}
    intent = risk.get("intent") or {}
    execution = snapshot.get("latest_execution_result") or {}
    order_request = execution.get("order_request") or {}
    response = execution.get("response") or {}
    reconciliation = snapshot.get("reconciliation", {}) or {}

    signal_side = _display_value(signal.get("signal", "-"))
    signal_status = "idle" if signal_side in {"-", "HOLD"} else "ready"
    risk_decision = _display_value(risk.get("decision", "-"))
    execution_status = _display_value(execution.get("status", "-"))
    demo_order_id = response.get("orderId") or response.get("clientOrderId") or order_request.get("client_order_id") or "-"
    reconciliation_status = reconciliation.get("status", "not-run")
    terminal = execution_status if execution_status not in {"-", "ACCEPTED"} else reconciliation_status

    return [
        _pipeline_row("Signal", signal_status, signal.get("timestamp_ms", ""), signal.get("model_version", "-"), signal_side),
        _pipeline_row("Risk", "allowed" if risk_decision == "ALLOW" else "blocked" if risk_decision == "BLOCK" else "idle", risk.get("timestamp_ms", ""), risk.get("reason", "-"), risk_decision),
        _pipeline_row("Intent", "ready" if intent else "idle", "", intent.get("side", "-") if intent else "-", intent.get("quote_size", "-") if intent else "-"),
        _pipeline_row("Test order", execution_status.lower() if execution_status != "-" else "idle", "", execution_status, order_request.get("client_order_id", "-")),
        _pipeline_row("Demo order", "sent" if demo_order_id != "-" else "idle", "", response.get("status", execution_status), demo_order_id),
        _pipeline_row("Reconciliation", reconciliation_status, reconciliation.get("checked_at_ms", ""), reconciliation.get("status", "not-run"), reconciliation.get("orphan_orders", 0)),
        _pipeline_row("Fill/Cancel/Reject", str(terminal).lower(), "", _terminal_reason(execution, reconciliation), terminal),
    ]


def _check_row(label: str, passed: bool, detail: Any, blocking: bool) -> dict[str, Any]:
    if passed:
        status = "pass"
    elif blocking:
        status = "fail"
    else:
        status = "warn"
    return {"check": label, "status": status, "detail": _display_value(detail), "blocking": blocking}


def _pipeline_row(step: str, status: Any, timestamp_ms: Any, detail: Any, reference: Any) -> dict[str, Any]:
    return {
        "step": step,
        "status": _display_value(status),
        "timestamp_ms": _display_value(timestamp_ms),
        "detail": _display_value(detail),
        "reference": _display_value(reference),
    }


def _terminal_reason(execution: dict[str, Any], reconciliation: dict[str, Any]) -> str:
    response = execution.get("response") or {}
    if response.get("msg"):
        return str(response["msg"])
    if reconciliation.get("needs_operator_action"):
        return "operator action required"
    if reconciliation.get("status") and reconciliation.get("status") != "not-run":
        return str(reconciliation["status"])
    return _display_value(execution.get("status", "-"))


def _display_value(value: Any) -> str:
    if hasattr(value, "value"):
        return str(value.value)
    if value is None or value == "":
        return "-"
    return str(value)


class DemoOrderReconciler:
    def __init__(self, adapter: BinanceSpotAdapter, lifecycle: OrderLifecycleStore):
        self.adapter = adapter
        self.lifecycle = lifecycle

    def reconcile(self, symbol: str) -> ReconciliationResult:
        events: list[dict[str, Any]] = []
        failures = 0
        open_orders: list[dict[str, Any]] = []
        try:
            open_orders = list(self.adapter.open_orders(symbol))
        except Exception as exc:
            failures += 1
            events.append({"type": "RECONCILIATION_FAILED", "message": str(exc)})
        known_client_ids = set(self.lifecycle.orders.keys())
        open_client_ids = {str(item.get("clientOrderId") or item.get("newClientOrderId") or "") for item in open_orders}
        for lifecycle in list(self.lifecycle.orders.values()):
            if lifecycle.status in TERMINAL_STATUSES:
                continue
            try:
                payload = self.adapter.query_order(symbol, order_id=lifecycle.order_id, client_order_id=lifecycle.client_order_id)
                self.lifecycle.apply_order_payload(payload)
                events.append({"type": "QUERY_ORDER", "client_order_id": lifecycle.client_order_id, "status": payload.get("status")})
            except Exception as exc:
                failures += 1
                lifecycle.status = "RECONCILIATION_FAILED"
                lifecycle.needs_reconciliation = True
                lifecycle.events.append({"type": "RECONCILIATION_FAILED", "message": str(exc)})
                events.append({"type": "RECONCILIATION_FAILED", "client_order_id": lifecycle.client_order_id, "message": str(exc)})
        orphan_count = 0
        for item in open_orders:
            client_id = str(item.get("clientOrderId") or item.get("newClientOrderId") or "")
            if client_id and client_id not in known_client_ids:
                orphan_count += 1
                lifecycle = self.lifecycle.record_external_order(client_id, symbol, str(item.get("side", "")))
                lifecycle.status = "ORPHAN_OPEN"
                lifecycle.needs_reconciliation = True
                lifecycle.order_id = int(item["orderId"]) if str(item.get("orderId", "")).isdigit() else lifecycle.order_id
                lifecycle.events.append({"type": "ORPHAN_OPEN", "payload": redact_payload(item)})
                events.append({"type": "ORPHAN_OPEN", "client_order_id": client_id, "status": item.get("status")})
        status = "ok" if failures == 0 and orphan_count == 0 else "needs_operator_action"
        return ReconciliationResult(status, len(known_client_ids), len(open_orders), orphan_count, failures, events)

    def clean_start_status(self, symbol: str) -> ReconciliationResult:
        try:
            open_orders = list(self.adapter.open_orders(symbol))
        except Exception as exc:
            return ReconciliationResult("error", len(self.lifecycle.orders), 0, 0, 1, [{"type": "CLEAN_START_FAILED", "message": str(exc)}])
        orphan_count = len(open_orders)
        events = [{"type": "ORPHAN_OPEN", "client_order_id": str(item.get("clientOrderId", "")), "status": item.get("status")} for item in open_orders]
        return ReconciliationResult("ok" if orphan_count == 0 else "needs_operator_action", len(self.lifecycle.orders), len(open_orders), orphan_count, 0, events)


class DemoAccountSync:
    def __init__(self, adapter: BinanceSpotAdapter):
        self.adapter = adapter

    def sync(self) -> DemoAccountSnapshot:
        try:
            payload = self.adapter.get_account_state()
            balances = [
                {
                    "asset": item.get("asset"),
                    "free": str(item.get("free", "0")),
                    "locked": str(item.get("locked", "0")),
                }
                for item in payload.get("balances", [])
                if Decimal(str(item.get("free", "0"))) != 0 or Decimal(str(item.get("locked", "0"))) != 0
            ]
            return DemoAccountSnapshot(
                "ok",
                bool(payload.get("canTrade")),
                str(payload.get("accountType", "")),
                balances[:50],
                int(time.time() * 1000),
            )
        except (BinanceAPIError, Exception) as exc:
            return DemoAccountSnapshot("error", None, "", [], int(time.time() * 1000), str(exc))


def should_pause_pilot(config: DemoPilotConfig, counters: DemoPilotCounters, now_ms: int | None = None) -> tuple[bool, str]:
    if counters.orders >= config.max_demo_orders:
        return True, "max demo orders reached"
    if counters.rejects > config.max_rejects:
        return True, "max rejects exceeded"
    if counters.api_errors > config.max_api_errors:
        return True, "max api errors exceeded"
    if counters.reconciliation_failures > config.max_reconciliation_failures:
        return True, "max reconciliation failures exceeded"
    if counters.elapsed_seconds(now_ms) >= config.duration_minutes * 60:
        return True, "pilot duration reached"
    return False, ""
