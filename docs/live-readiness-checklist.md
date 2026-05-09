# Live Readiness Checklist

Live trading is blocked until every item is checked and documented.

- [ ] Backtest is positive out-of-sample after fees and slippage.
- [ ] Walk-forward evaluation is documented.
- [ ] Paper trading ran for the agreed period without reconciliation failures.
- [ ] Spot Testnet order lifecycle is validated.
- [ ] Kill switch has been tested.
- [ ] Daily max loss block has been tested.
- [ ] Order status unknown handling has been tested.
- [ ] API keys have minimal permissions.
- [ ] Withdrawal permission is disabled.
- [ ] IP restrictions are configured where available.
- [ ] Secret scan passes.
- [ ] Logs redact keys, signatures and auth headers.
- [ ] Position size, max trades per day and daily max loss are small and explicit.
- [ ] Manual approval phrase is set only for the live launch session.

