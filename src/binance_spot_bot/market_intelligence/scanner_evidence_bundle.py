from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from binance_spot_bot.redaction import redact_payload
from .multi_symbol_paper_analytics import run_multi_symbol_paper_analytics
from .public_endpoint_policy import NO_FINANCIAL_ADVICE_STATEMENT, NO_LIVE_STATEMENT, build_public_endpoint_policy_report, public_endpoint_policy_report_to_dict
from .scanner_presets import get_scanner_preset, scanner_presets_payload
from .symbol_ranking import rank_symbols
from .symbol_universe import symbol_universe_to_dict, build_symbol_universe
from .watchlist_scanner import run_watchlist_scan


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def export_market_intelligence_evidence(root: Path | str = ".", preset_id: str = "majors_overview") -> dict[str, Any]:
    root = Path(root)
    preset = get_scanner_preset(preset_id)
    scan = run_watchlist_scan(preset.symbols, root=root, preset=preset_id)
    ranking = rank_symbols(list(scan.get("metrics", [])), preset.ranking_dimension)
    artifacts: dict[str, Any] = {
        "safety_contract": {"status": "ok", "public_only": True, "no_financial_advice_statement": NO_FINANCIAL_ADVICE_STATEMENT, "live_trading_enabled": False},
        "public_endpoint_policy": public_endpoint_policy_report_to_dict(build_public_endpoint_policy_report()),
        "symbol_universe": symbol_universe_to_dict(build_symbol_universe()),
        "scanner_presets": scanner_presets_payload(),
        "watchlist_scan": scan,
        "ranking": ranking,
        "paper_analytics": run_multi_symbol_paper_analytics(preset.symbols, root=root),
        "no_live_proof": {"no_live_statement": NO_LIVE_STATEMENT, "live_trading_enabled": False},
    }
    run_id = str(int(time.time() * 1000))
    out = root / "data" / "market-intelligence" / "evidence" / run_id
    files_dir = out / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    files = []
    for name, payload in artifacts.items():
        text = json.dumps(redact_payload(payload), indent=2, default=str)
        path = files_dir / f"{name}.json"
        path.write_text(text, encoding="utf-8")
        files.append({"name": name, "path": str(path), "sha256": _hash(text)})
    manifest = redact_payload({"status": "ok", "run_id": run_id, "files": files, "no_live_statement": NO_LIVE_STATEMENT, "no_financial_advice_statement": NO_FINANCIAL_ADVICE_STATEMENT, "live_trading_enabled": False})
    manifest_path = out / "market_intelligence_evidence_manifest.json"
    summary_path = out / "market_intelligence_evidence_summary.md"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_path.write_text(f"# Market Intelligence Evidence\n\nStatus: ok\n\n{NO_FINANCIAL_ADVICE_STATEMENT}\n", encoding="utf-8")
    return {"status": "ok", "run_id": run_id, "manifest": str(manifest_path), "summary": str(summary_path), "files": files, "live_trading_enabled": False}
