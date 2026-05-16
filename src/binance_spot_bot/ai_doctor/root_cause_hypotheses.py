from __future__ import annotations

from typing import Any


def build_root_cause_hypotheses(matches: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    matches = matches or []
    hypotheses = [{
        "hypothesis_id": "hyp-" + str(index),
        "title": match.get("title", "Unknown issue"),
        "confidence": match.get("confidence", "low"),
        "evidence_refs": [match.get("issue_id", "")],
        "suspect_files": match.get("suspect_files", []),
        "safest_next_step": match.get("recommended_fix", "investigate_first"),
        "recommended_tests": match.get("recommended_tests", []),
    } for index, match in enumerate(matches, start=1)]
    return {"status": "ok", "hypotheses": hypotheses or [{"hypothesis_id": "hyp-unknown", "title": "unknown/needs more evidence", "confidence": "low"}], "live_trading_enabled": False}

