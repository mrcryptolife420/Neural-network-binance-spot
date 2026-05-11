from pathlib import Path
def roadmap_move_plan(src: Path, dst: Path): return {"status": "ready" if src.exists() else "blocked", "source": str(src), "destination": str(dst), "preview_only": True, "live_trading_enabled": False}
