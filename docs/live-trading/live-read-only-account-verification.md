# Live Read-Only Account Verification

The read-only verifier checks live credentials, live base URL, permissions, balance summaries, server-time drift, and API key fingerprinting.

It does not place, cancel, or query live orders.

Use:

```powershell
python -m binance_spot_bot.cli live-account-verify --json
```
