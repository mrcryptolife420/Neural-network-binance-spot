# Security Runbook

Support bundles and operator diagnostics must keep live trading disabled and redact API keys, secrets and token-like values before writing artifacts. Use `spot-bot security-scan` after exporting a support bundle when sharing debugging evidence.

## Defaults

- Live trading is disabled by default.
- `KILL_SWITCH=true` blocks trading.
- Withdrawal permissions must remain disabled for every Binance API key.
- API keys must come from environment variables or a secret manager, never from repository files.

## Key compromise response

1. Set `KILL_SWITCH=true`.
2. Stop all bot processes.
3. Cancel open orders manually in Binance if needed.
4. Revoke the suspected Binance API key.
5. Rotate any related keys.
6. Review `data/audit/events.jsonl` and logs for unexpected actions.
7. Create a post-mortem note before enabling any new key.

## Before testnet

- Use Spot Testnet credentials only.
- Confirm `TRADING_MODE=testnet`.
- Confirm `LIVE_TRADING_ENABLED=false`.
- Confirm no real key is present in repository files.
- Run Demo Execution Drill preview and test-order-only before any confirmed Demo Spot order.
- Never use API keys with withdrawal permissions.
- Cancel or reconcile open Demo Spot orders before continuing after unknown or timeout states.

## Before live pilot

Live pilot is out of MVP scope. It requires all live-readiness checklist items in `docs/live-readiness-checklist.md` and manual approval.
