# Live Endpoint Policy

The endpoint policy is phase-aware.

- `read_only`: public and account-state reads only
- `dry_run`: public reads plus local previews
- `preview`: local preview and optional test-order checks
- `first_order`: one confirmed tiny first-order path

Use:

```powershell
python -m binance_spot_bot.cli live-endpoint-policy --phase dry_run --json
```
