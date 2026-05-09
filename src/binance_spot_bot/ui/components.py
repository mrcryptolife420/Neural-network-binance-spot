from __future__ import annotations

from typing import Any

import streamlit as st


def render_badges(items: dict[str, Any]) -> None:
    cols = st.columns(max(1, len(items)))
    for col, (label, value) in zip(cols, items.items()):
        col.metric(label, value)


def render_table(title: str, rows: list[dict[str, Any]]) -> None:
    st.subheader(title)
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.caption("No records yet.")


def render_debug(label: str, payload: Any) -> None:
    with st.expander(label):
        st.json(payload)


def render_alert_list(rows: list[dict[str, Any]]) -> None:
    render_table(
        "Alerts",
        [
            {
                "severity": row.get("severity"),
                "name": row.get("name"),
                "action": row.get("action"),
                "message": row.get("message"),
            }
            for row in rows
        ],
    )
