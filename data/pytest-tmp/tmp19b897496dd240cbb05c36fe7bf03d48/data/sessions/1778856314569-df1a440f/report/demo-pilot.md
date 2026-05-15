# Demo Pilot Report 1778856314569-df1a440f

## Executive summary
- Mode: demo
- Symbol: BTCUSDT
- Status: stopped
- PnL: 0.162765016096573875124875
- Max drawdown: 2.0044837638154451248751250
- Pilot preset: smoke
- Orders: 0 / 5
- Rejects: 0 / 2
- Reconciliation: not-run
- Cancel-on-stop events: 0

## Operator checklist
| check | status | detail | blocking |
| --- | --- | --- | --- |
| Profile | fail | unknown | True |
| Credentials | fail | not loaded | True |
| Connection | fail | not tested | True |
| Server time | warn | test connection first | False |
| Account canTrade | fail | not synced | True |
| Clean start | pass | not-run | True |
| No orphan orders | pass | 0 orphan orders | True |
| Risk limits | fail | missing limits | True |
| Pilot preset | pass | smoke | False |
| Armed | warn | explicit arm required | False |

## Signal to order pipeline
| step | status | timestamp_ms | detail | reference |
| --- | --- | --- | --- | --- |
| Signal | idle | - | - | - |
| Risk | idle | - | - | - |
| Intent | idle | - | - | - |
| Test order | blocked | - | BLOCKED | - |
| Demo order | idle | - | BLOCKED | - |
| Reconciliation | not-run | - | not-run | 0 |
| Fill/Cancel/Reject | blocked | - | BLOCKED | BLOCKED |

## Orders and reconciliation
- Orders recorded: 75
- Alerts recorded: 52
- Orphan orders: 0
- Failures: 0
