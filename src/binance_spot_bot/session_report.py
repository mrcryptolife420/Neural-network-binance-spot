from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .demo_pilot import operator_checklist, pipeline_rows
from .pilot_orchestrator import pilot_acceptance_markdown, pilot_acceptance_payload
from .redaction import redact_payload
from .session_store import SessionStore, SessionSummary


def export_session_report(store: SessionStore, session_id: str, output_dir: Path | None = None) -> dict[str, str]:
    summary = store.load_summary(session_id)
    snapshots = store.load_events(session_id, "snapshots.jsonl")
    fills = store.load_events(session_id, "fills.jsonl")
    alerts = store.load_events(session_id, "alerts.jsonl")
    orders = store.load_events(session_id, "orders.jsonl")
    root = output_dir or store.root / session_id / "report"
    root.mkdir(parents=True, exist_ok=True)
    summary_json = root / "summary.json"
    summary_md = root / "summary.md"
    fills_csv = root / "fills.csv"
    equity_csv = root / "equity.csv"
    alerts_jsonl = root / "alerts.jsonl"
    orders_jsonl = root / "orders.jsonl"
    config_json = root / "config-redacted.json"
    demo_pilot_json = root / "demo-pilot.json"
    demo_pilot_md = root / "demo-pilot.md"
    demo_pilot_payload = _demo_pilot_report_payload(summary, snapshots, orders, alerts)
    pilot_acceptance_json = root / "pilot-acceptance.json"
    pilot_acceptance_md = root / "pilot-acceptance.md"
    acceptance_payload = pilot_acceptance_payload(summary, snapshots, orders, alerts)
    summary_json.write_text(json.dumps(redact_payload(asdict(summary)), indent=2, default=str), encoding="utf-8")
    summary_md.write_text(_summary_markdown(summary, len(snapshots), len(fills)), encoding="utf-8")
    _write_csv(fills_csv, fills)
    _write_csv(equity_csv, _equity_rows(snapshots))
    _write_jsonl(alerts_jsonl, alerts)
    _write_jsonl(orders_jsonl, orders)
    config_json.write_text(json.dumps(redact_payload(summary.metadata), indent=2, default=str), encoding="utf-8")
    demo_pilot_json.write_text(json.dumps(redact_payload(demo_pilot_payload), indent=2, default=str), encoding="utf-8")
    demo_pilot_md.write_text(_demo_pilot_markdown(redact_payload(demo_pilot_payload)), encoding="utf-8")
    pilot_acceptance_json.write_text(json.dumps(redact_payload(acceptance_payload), indent=2, default=str), encoding="utf-8")
    pilot_acceptance_md.write_text(pilot_acceptance_markdown(redact_payload(acceptance_payload)), encoding="utf-8")
    return {
        "summary_json": str(summary_json),
        "summary_md": str(summary_md),
        "fills_csv": str(fills_csv),
        "equity_csv": str(equity_csv),
        "alerts_jsonl": str(alerts_jsonl),
        "orders_jsonl": str(orders_jsonl),
        "config_redacted_json": str(config_json),
        "demo_pilot_json": str(demo_pilot_json),
        "demo_pilot_md": str(demo_pilot_md),
        "pilot_acceptance_json": str(pilot_acceptance_json),
        "pilot_acceptance_md": str(pilot_acceptance_md),
    }


def _summary_markdown(summary: SessionSummary, snapshots: int, fills: int) -> str:
    return "\n".join(
        [
            f"# Session {summary.session_id}",
            "",
            f"- Mode: {summary.mode}",
            f"- Symbol: {summary.symbol}",
            f"- Interval: {summary.interval}",
            f"- Status: {summary.status}",
            f"- PnL: {summary.pnl}",
            f"- Max drawdown: {summary.max_drawdown}",
            f"- Trades: {summary.trades}",
            f"- Blocks: {summary.blocks}",
            f"- Snapshots: {snapshots}",
            f"- Fills: {fills}",
            "",
        ]
    )


def _equity_rows(snapshots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in snapshots:
        if "equity" in item:
            rows.append({"timestamp_ms": item.get("timestamp_ms", ""), "equity": item.get("equity")})
    return rows


def _demo_pilot_report_payload(
    summary: SessionSummary,
    snapshots: list[dict[str, Any]],
    orders: list[dict[str, Any]],
    alerts: list[dict[str, Any]],
) -> dict[str, Any]:
    latest_snapshot = snapshots[-1] if snapshots else {}
    payload = dict(latest_snapshot)
    payload.setdefault("demo_pilot", summary.metadata.get("demo_pilot", {}))
    payload.setdefault("reconciliation", summary.metadata.get("reconciliation", {}))
    payload.setdefault("cancel_on_stop_status", summary.metadata.get("cancel_on_stop_status", []))
    payload.setdefault("latest_execution_result", orders[-1] if orders else {})
    return {
        "session": {
            "session_id": summary.session_id,
            "mode": summary.mode,
            "symbol": summary.symbol,
            "interval": summary.interval,
            "status": summary.status,
            "pnl": str(summary.pnl),
            "max_drawdown": str(summary.max_drawdown),
        },
        "demo_pilot": payload.get("demo_pilot", {}),
        "connection": payload.get("demo_connection", {}),
        "account": payload.get("demo_account", {}),
        "reconciliation": payload.get("reconciliation", {}),
        "operator_checklist": operator_checklist(payload),
        "pipeline": pipeline_rows(payload),
        "cancel_on_stop_status": payload.get("cancel_on_stop_status", []),
        "orders": orders,
        "alerts": alerts,
        "latest_snapshot": latest_snapshot,
    }


def _demo_pilot_markdown(payload: dict[str, Any]) -> str:
    session = payload.get("session", {})
    pilot = payload.get("demo_pilot", {})
    config = pilot.get("config", {}) if isinstance(pilot, dict) else {}
    counters = pilot.get("counters", {}) if isinstance(pilot, dict) else {}
    reconciliation = payload.get("reconciliation", {})
    return "\n".join(
        [
            f"# Demo Pilot Report {session.get('session_id', '')}",
            "",
            "## Executive summary",
            f"- Mode: {session.get('mode', '-')}",
            f"- Symbol: {session.get('symbol', '-')}",
            f"- Status: {session.get('status', '-')}",
            f"- PnL: {session.get('pnl', '-')}",
            f"- Max drawdown: {session.get('max_drawdown', '-')}",
            f"- Pilot preset: {config.get('pilot_name', '-')}",
            f"- Orders: {counters.get('orders', 0)} / {config.get('max_demo_orders', '-')}",
            f"- Rejects: {counters.get('rejects', 0)} / {config.get('max_rejects', '-')}",
            f"- Reconciliation: {reconciliation.get('status', 'not-run')}",
            f"- Cancel-on-stop events: {len(payload.get('cancel_on_stop_status', []))}",
            "",
            "## Operator checklist",
            _markdown_table(payload.get("operator_checklist", [])),
            "",
            "## Signal to order pipeline",
            _markdown_table(payload.get("pipeline", [])),
            "",
            "## Orders and reconciliation",
            f"- Orders recorded: {len(payload.get('orders', []))}",
            f"- Alerts recorded: {len(payload.get('alerts', []))}",
            f"- Orphan orders: {reconciliation.get('orphan_orders', 0)}",
            f"- Failures: {reconciliation.get('failures', 0)}",
            "",
        ]
    )


def _markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = sorted({key for row in rows for key in row.keys()})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if fields:
            writer.writeheader()
            writer.writerows(redact_payload(rows))


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in redact_payload(rows):
            handle.write(json.dumps(row, default=str, sort_keys=True) + "\n")
