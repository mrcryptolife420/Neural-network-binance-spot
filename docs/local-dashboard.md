# Local Dashboard

Roadmap 002 adds a local visual operator dashboard on top of the existing safe bot modules. It does not enable live trading.

## Install UI dependencies

```powershell
pip install -e ".[ui]"
```

The core tests and CLI do not require UI dependencies.

## Safe first start

```powershell
$env:PYTHONPATH="src"
python -m binance_spot_bot.cli run-local --mode demo --symbol BTCUSDT --steps 50
```

This runs the local runtime with deterministic demo candles and writes audit events under `data/audit/`.

## Start visual dashboard V2

```powershell
$env:PYTHONPATH="src"
python -m binance_spot_bot.cli control-center
```

On Windows, double-click `Start Bot Dashboard.cmd` or `Start-Neural-Binance-Bot.cmd`.

The dashboard opens in the browser and shows:

- candles;
- signal markers;
- paper fills;
- equity;
- latest risk decision;
- block reasons;
- audit tail;
- health metrics;
- testnet readiness checks.

## Modes

- `demo`: local deterministic replay, no API keys, no network.
- `paper`: read-only Binance candles when available, fallback/error state when unavailable, paper execution only.
- `testnet-readiness`: shows whether credentials and safety settings are ready for Spot Testnet checks.

`live` is intentionally not selectable in the dashboard.

## Controls

- `Start / run`: process replay ticks continuously.
- `Pause`: stop automatic stepping.
- `Single step`: process exactly one tick.
- `Reset runtime`: rebuild the runtime with current controls.

## Troubleshooting

If Dashboard V2 dependencies are missing, the Windows one-click launcher installs the local `.[ui]` package automatically. Manual install:

```powershell
python -m pip install -e ".[ui]"
```

If imports fail:

```powershell
$env:PYTHONPATH="src"
```

If Binance read-only paper mode fails, use demo mode first. Paper mode must not require signed endpoints or credentials.

## Safety

The dashboard always displays `LIVE TRADING DISABLED`. It never exposes a live order button and it does not duplicate risk logic. All trade decisions flow through the existing `RiskEngine` and `ExecutionEngine`.

Roadmap 015 adds the operator flow on top of this dashboard:

- the header shows live-disabled, mode, profile, session status and readiness;
- Demo Spot Trading uses local paper fills only;
- Strategy Lab explains risk blocks and signals without changing risk rules;
- Research shows scanner ranking and local exports;
- Portfolio shows paper account state from the same accounting source as reports;
- Readiness records evidence and keeps `live_allowed=false`.

For a long-running local paper smoke:

```powershell
$env:PYTHONPATH="src"
python -m binance_spot_bot.cli paper-session --symbol BTCUSDT --minutes 15 --max-steps 200 --source demo
```

The command writes session summaries, alerts, orders, fills and report artifacts under `data/sessions/<session-id>/`.
