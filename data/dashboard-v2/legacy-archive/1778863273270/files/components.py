from __future__ import annotations

import json
from typing import Any

import streamlit as st

from binance_spot_bot.redaction import redact_payload

MAX_TABLE_ROWS = 250
MAX_DEBUG_CHARS = 12000


def limit_table_rows(rows: list[dict[str, Any]], *, max_rows: int = MAX_TABLE_ROWS) -> tuple[list[dict[str, Any]], bool]:
    if len(rows) <= max_rows:
        return rows, False
    return rows[:max_rows], True


def limit_debug_payload(payload: Any, *, max_chars: int = MAX_DEBUG_CHARS) -> dict[str, Any]:
    redacted = redact_payload(payload)
    text = json.dumps(redacted, default=str, sort_keys=True)
    if len(text) <= max_chars:
        return {"payload": redacted, "truncated": False, "original_chars": len(text), "live_trading_enabled": False}
    return {
        "payload": {"preview": text[:max_chars], "truncated": True},
        "truncated": True,
        "original_chars": len(text),
        "max_chars": max_chars,
        "live_trading_enabled": False,
    }


def render_plotly_chart(figure: Any, *, key: str, use_container_width: bool = True) -> None:
    if not key or not key.strip():
        raise ValueError("Plotly charts must use a stable non-empty Streamlit key")
    if figure is None:
        st.info("Chart unavailable.")
        return
    st.plotly_chart(figure, use_container_width=use_container_width, key=key)


def render_badges(items: dict[str, Any] | list[dict[str, Any]]) -> None:
    if isinstance(items, list):
        pairs = [(str(row.get("label", "")), row.get("value", "")) for row in items]
    else:
        pairs = list(items.items())
    cols = st.columns(max(1, len(pairs)))
    for col, (label, val) in zip(cols, pairs):
        col.metric(label, val)


def render_table(title: str, rows: list[dict[str, Any]], *, max_rows: int = MAX_TABLE_ROWS) -> None:
    st.subheader(title)
    limited_rows, truncated = limit_table_rows(rows, max_rows=max_rows)
    if limited_rows:
        st.dataframe(limited_rows, use_container_width=True, hide_index=True)
        if truncated:
            st.caption(f"Showing first {len(limited_rows)} of {len(rows)} rows.")
    else:
        st.caption("No records yet.")


def render_debug(label: str, payload: Any) -> None:
    with st.expander(label):
        limited = limit_debug_payload(payload)
        st.json(limited["payload"])
        if limited["truncated"]:
            st.caption(f"Debug payload truncated at {limited['max_chars']} characters.")


def render_alert_list(rows: list[dict[str, Any]]) -> None:
    if not rows:
        st.caption("No alerts.")
        return
    st.dataframe(
        [
            {
                "severity": row.get("severity"),
                "name": row.get("name"),
                "action": row.get("action"),
                "msg": row.get("msg") or row.get("message"),
            }
            for row in rows
        ],
        use_container_width=True,
        hide_index=True,
    )
