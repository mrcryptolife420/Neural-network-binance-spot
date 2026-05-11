from __future__ import annotations

import hashlib
from typing import Any


def split_assignment(symbol: str, alloc_split: dict[str, str], *, seed: int = 7, bucket_key: str = "") -> str:
    challenger_pct = int(float(alloc_split.get("challenger", "0")))
    if challenger_pct <= 0:
        return "champion"
    if challenger_pct >= 100:
        return "challenger"
    raw = f"{seed}:{symbol.upper()}:{bucket_key}".encode("utf-8")
    bucket = int(hashlib.sha256(raw).hexdigest()[:8], 16) % 100
    return "challenger" if bucket < challenger_pct else "champion"


def build_split_table(
    symbols: list[str],
    alloc_split: dict[str, str],
    *,
    seed: int = 7,
    split_type: str = "allocation",
    time_slices: list[str] | None = None,
    canary_symbols: list[str] | None = None,
) -> dict[str, Any]:
    if split_type not in {"allocation", "symbol", "time_slice", "canary"}:
        raise ValueError("invalid split_type")
    normalized = sorted({symbol.strip().upper() for symbol in symbols if symbol.strip()})
    if not normalized:
        raise ValueError("symbols are required")
    _validate_alloc_split(alloc_split)
    canaries = {symbol.upper() for symbol in (canary_symbols or [])}
    rows: list[dict[str, Any]] = []
    for symbol in normalized:
        if split_type == "canary":
            variant = "challenger" if symbol in canaries else "champion"
            rows.append({"symbol": symbol, "variant": variant, "split_type": split_type})
        elif split_type == "time_slice":
            slices = time_slices or ["00:00-06:00", "06:00-12:00", "12:00-18:00", "18:00-24:00"]
            for slice_id in slices:
                rows.append(
                    {
                        "symbol": symbol,
                        "time_slice": slice_id,
                        "variant": split_assignment(symbol, alloc_split, seed=seed, bucket_key=slice_id),
                        "split_type": split_type,
                    }
                )
        elif split_type == "symbol":
            rows.append({"symbol": symbol, "variant": split_assignment(symbol, alloc_split, seed=seed), "split_type": split_type})
        else:
            rows.append({"symbol": symbol, "variant": split_assignment(symbol, alloc_split, seed=seed), "split_type": split_type})
    guardrails = {
        "no_signed_endpoints": True,
        "paper_only": True,
        "deterministic_seed": seed,
        "allocation_total": int(float(alloc_split.get("champion", "0"))) + int(float(alloc_split.get("challenger", "0"))),
    }
    return {
        "status": "ready",
        "seed": seed,
        "split_type": split_type,
        "assignments": rows,
        "guardrails": guardrails,
        "live_trading_enabled": False,
    }


def _validate_alloc_split(alloc_split: dict[str, str]) -> None:
    champion = int(float(alloc_split.get("champion", "0")))
    challenger = int(float(alloc_split.get("challenger", "0")))
    if champion < 0 or challenger < 0 or champion + challenger != 100:
        raise ValueError("allocation split must be non-negative and equal 100")
