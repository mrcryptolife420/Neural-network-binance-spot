from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redaction import redact_payload


def export_notebook(title: str, payload: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe = redact_payload(payload)
    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [f"# {title}\n"]},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [f"payload = {json.dumps(safe, indent=2, default=str)}\n", "payload\n"]},
        ],
        "metadata": {"language_info": {"name": "python"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    return path
