from __future__ import annotations

from pathlib import Path

import pytest

from binance_spot_bot.ui.chart_registry import all_chart_keys
from binance_spot_bot.ui.components import render_plotly_chart


ROOT = Path(__file__).resolve().parents[1]


def test_chart_registry_keys_are_unique() -> None:
    keys = all_chart_keys()
    assert keys
    assert len(keys) == len(set(keys))


def test_plotly_helper_requires_stable_key() -> None:
    with pytest.raises(ValueError):
        render_plotly_chart(None, key="")


def test_streamlit_plotly_calls_are_centralized_or_keyed() -> None:
    offenders: list[str] = []
    for path in (ROOT / "src" / "binance_spot_bot" / "ui").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "st.plotly_chart(" not in text:
            continue
        for index, line in enumerate(text.splitlines(), start=1):
            if "st.plotly_chart(" not in line:
                continue
            window = "\n".join(text.splitlines()[index - 1 : index + 8])
            if path.name != "components.py" and "key=" not in window:
                offenders.append(f"{path.relative_to(ROOT)}:{index}")
    assert offenders == []


def test_streamlit_app_uses_plotly_helper_not_direct_calls() -> None:
    app = ROOT / "src" / "binance_spot_bot" / "ui" / "streamlit_app.py"
    assert "st.plotly_chart(" not in app.read_text(encoding="utf-8")
