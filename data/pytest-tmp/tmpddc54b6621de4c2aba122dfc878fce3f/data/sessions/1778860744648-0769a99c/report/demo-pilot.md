# Demo Pilot Report 1778860744648-0769a99c

## Executive summary
- Mode: demo
- Symbol: BTCUSDT
- Status: stopped
- PnL: 0
- Max drawdown: 0
- Pilot preset: smoke
- Orders: 0 / 5
- Rejects: 0 / 2
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
| Reconciliation | ok | 1778860744699 | ok | 0 |
| Fill/Cancel/Reject | ok | - | ok | ok |

## Orders and reconciliation
- Orders recorded: 2
- Alerts recorded: 2
- Orphan orders: 0
- Failures: 0
