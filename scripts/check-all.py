from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from binance_spot_bot.check_all import payload_for, print_payload, run_checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args()
    payload = payload_for(run_checks(ROOT, skip_tests=args.skip_tests))
    print_payload(payload, as_json=args.json)
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
