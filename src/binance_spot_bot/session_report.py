from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

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
    summary_json.write_text(json.dumps(redact_payload(asdict(summary)), indent=2, default=str), encoding="utf-8")
    summary_md.write_text(_summary_markdown(summary, len(snapshots), len(fills)), encoding="utf-8")
    _write_csv(fills_csv, fills)
    _write_csv(equity_csv, _equity_rows(snapshots))
    _write_jsonl(alerts_jsonl, alerts)
    _write_jsonl(orders_jsonl, orders)
    config_json.write_text(json.dumps(redact_payload(summary.metadata), indent=2, default=str), encoding="utf-8")
    return {
        "summary_json": str(summary_json),
        "summary_md": str(summary_md),
        "fills_csv": str(fills_csv),
        "equity_csv": str(equity_csv),
        "alerts_jsonl": str(alerts_jsonl),
        "orders_jsonl": str(orders_jsonl),
        "config_redacted_json": str(config_json),
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
