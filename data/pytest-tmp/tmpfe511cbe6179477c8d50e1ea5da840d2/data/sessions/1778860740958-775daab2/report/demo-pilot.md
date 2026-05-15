# Demo Pilot Report 1778860740958-775daab2

## Executive summary
- Mode: demo
- Symbol: BTCUSDT
- Status: stopped
- PnL: 0.0000
- Max drawdown: 0
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
- Orders recorded: 1
- Alerts recorded: 4
- Orphan orders: 0
- Failures: 0
