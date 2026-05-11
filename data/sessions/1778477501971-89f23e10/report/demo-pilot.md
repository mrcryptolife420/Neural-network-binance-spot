# Demo Pilot Report 1778477501971-89f23e10

## Executive summary
- Mode: demo
- Symbol: BTCUSDT
- Status: stopped
- PnL: 10.0356215210000000
- Max drawdown: 0.0082356180000000
- Pilot preset: smoke
- Orders: 4 / 5
- Rejects: 3 / 2
- Reconciliation: ok
- Cancel-on-stop events: 0

## Operator checklist
| check | status | detail | blocking |
| --- | --- | --- | --- |
| Profile | fail | unknown | True |
| Credentials | fail | not loaded | True |
| Connection | fail | not tested | True |
| Server time | warn | test connection first | False |
| Account canTrade | fail | not synced | True |
| Clean start | pass | ok | True |
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
| Test order | ok | - | ok | - |
| Demo order | idle | - | ok | - |
| Reconciliation | ok | 1778477701891 | ok | 0 |
| Fill/Cancel/Reject | ok | - | ok | ok |

## Orders and reconciliation
- Orders recorded: 15
- Alerts recorded: 9
- Orphan orders: 0
- Failures: 0
