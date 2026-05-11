from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_operator_diagnostics_docs_exist_and_keep_live_disabled_language() -> None:
    docs = [
        ROOT / "docs" / "operator-diagnostics.md",
        ROOT / "docs" / "support-bundle.md",
    ]
    for path in docs:
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "live trading" in text
        assert "disabled" in text
