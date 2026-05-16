# First Live Order Gate

The first-order gate is blocked by default and requires all live-safety gates plus exact confirmation.

The implementation uses a fake adapter in tests and disarms after the attempt. No unattended live loop is allowed.

Use:

```powershell
python -m binance_spot_bot.cli live-first-order-execute --confirm I_UNDERSTAND_THIS_WILL_PLACE_A_REAL_BINANCE_SPOT_ORDER --json
```
