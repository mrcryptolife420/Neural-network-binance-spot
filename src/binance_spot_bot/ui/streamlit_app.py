from __future__ import annotations

import json
import sys


def main() -> None:
    payload = {
        "status": "removed",
        "dashboard": "dashboard-v2",
        "message": "The Streamlit dashboard has been removed. Start Dashboard V2 with Start Bot Dashboard.cmd or Start-Neural-Binance-Bot.cmd.",
        "start_commands": [
            "Start Bot Dashboard.cmd",
            "Start-Neural-Binance-Bot.cmd",
            "python -m binance_spot_bot.cli control-center",
        ],
        "live_trading_enabled": False,
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    sys.exit(main())
