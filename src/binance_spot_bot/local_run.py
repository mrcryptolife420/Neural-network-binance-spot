from __future__ import annotations

import argparse
import json

from .config import BotSettings
from .runtime import BotRuntime, RuntimeOptions, snapshot_to_dict


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m binance_spot_bot.local_run")
    parser.add_argument("--mode", choices=["demo", "paper", "testnet-readiness"], default="demo")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="1m")
    parser.add_argument("--scenario", default="sideways")
    parser.add_argument("--steps", type=int, default=50)
    args = parser.parse_args()

    runtime = BotRuntime(
        BotSettings.from_env(),
        RuntimeOptions(
            mode=args.mode,
            symbol=args.symbol,
            interval=args.interval,
            scenario=args.scenario,
        ),
    )
    snapshot = runtime.run_steps(args.steps)
    payload = snapshot_to_dict(snapshot)
    print(
        json.dumps(
            {
                "mode": payload["mode"],
                "symbol": payload["symbol"],
                "status": payload["status"],
                "message": payload["message"],
                "equity": str(payload["equity"]),
                "paper_position": str(payload["paper_position"]),
                "signals": payload["metrics"]["signals"],
                "block_reasons": payload["metrics"]["block_reasons"],
                "fills": len(payload["fills"]),
            },
            default=str,
        )
    )


if __name__ == "__main__":
    main()
