from pathlib import Path
def test_inventory(root: Path): return {"status": "ready", "tests": sorted(str(p) for p in root.glob("tests/test_*.py")), "live_trading_enabled": False}
