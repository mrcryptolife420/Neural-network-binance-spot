# Demo Order Lifecycle Drill

Use the lifecycle drill to prove that a Demo Spot order can be prepared, tested, placed, queried and canceled under operator control.

## CLI

```powershell
spot-bot demo-execution-preview --symbol BTCUSDT --side BUY --quote-size 10
spot-bot demo-execution-test-order --symbol BTCUSDT --side BUY --quote-size 10
spot-bot demo-execution-place --symbol BTCUSDT --side BUY --quote-size 10 --armed --confirm-demo-order
spot-bot demo-execution-query --symbol BTCUSDT --client-order-id <id>
spot-bot demo-execution-cancel --symbol BTCUSDT --order-id <id> --confirm-cancel
spot-bot demo-execution-report
```

## Dashboard

Open Demo Spot Trading and use `Demo Execution Drill`.

Expected operator sequence:

1. Preview order.
2. Test order only.
3. Confirm demo order.
4. Place demo order only if Demo Spot is armed and gates pass.
5. Query status.
6. Confirm cancel before canceling.
7. Export drill evidence.

Unknown or timeout states require reconciliation before continuing.
