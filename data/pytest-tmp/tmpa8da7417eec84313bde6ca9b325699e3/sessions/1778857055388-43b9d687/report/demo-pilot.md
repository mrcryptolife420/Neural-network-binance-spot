# Demo Pilot Report 1778857055388-43b9d687

## Executive summary
- Mode: demo
- Symbol: BTCUSDT
- Status: running
- PnL: 0
- Max drawdown: 0
- Pilot preset: -
- Orders: 0 / -
- Rejects: 0 / -
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
| Pilot preset | warn | not selected | False |
| Armed | warn | explicit arm required | False |

## Signal to order pipeline
| step | status | timestamp_ms | detail | reference |
| --- | --- | --- | --- | --- |
| Signal | idle | - | - | - |
| Risk | idle | - | - | - |
| Intent | idle | - | - | - |
| Test order | idle | - | - | - |
| Demo order | idle | - | - | - |
| Reconciliation | not-run | - | not-run | 0 |
| Fill/Cancel/Reject | not-run | - | - | not-run |

## Orders and reconciliation
- Orders recorded: 0
- Alerts recorded: 0
- Orphan orders: 0
- Failures: 0
