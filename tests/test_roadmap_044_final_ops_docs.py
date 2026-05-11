from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_operator_ops_docs_exist() -> None:
    for name in ["operator-diagnostics.md", "support-bundle.md", "operator-local-ops.md"]:
        path = ROOT / "docs" / name
        assert path.exists()
        assert "live trading" in path.read_text(encoding="utf-8").lower()
