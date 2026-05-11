from __future__ import annotations

from typing import Any

import streamlit as st


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
