# Demo Pilot Report 1778858446797-9f3705d4

## Executive summary
- Mode: demo
- Symbol: BTCUSDT
- Status: stopped
- PnL: 0
- Max drawdown: 0
- Pilot preset: smoke
- Orders: 0 / 5
- Rejects: 0 / 2
- Reconciliation: needs_operator_action
- Cancel-on-stop events: 1

## Operator checklist
| check | status | detail | blocking |
| --- | --- | --- | --- |
| Profile | fail | unknown | True |
| Credentials | fail | not loaded | True |
| Connection | fail | not tested | True |
| Server time | warn | test connection first | False |
| Account canTrade | fail | not synced | True |
| Clean start | fail | needs_operator_action | True |
| No orphan orders | fail | 1 orphan orders | True |
| Risk limits | fail | missing limits | True |
| Pilot preset | pass | smoke | False |
| Armed | warn | explicit arm required | False |

## Signal to order pipeline
| step | status | timestamp_ms | detail | reference |
| --- | --- | --- | --- | --- |
| Signal | idle | - | - | - |
| Risk | idle | - | - | - |
| Intent | idle | - | - | - |
| Test order | needs_operator_action | - | needs_operator_action | - |
| Demo order | idle | - | needs_operator_action | - |
| Reconciliation | needs_operator_action | 1778858446825 | needs_operator_action | 1 |
| Fill/Cancel/Reject | needs_operator_action | - | operator action required | needs_operator_action |

## Orders and reconciliation
- Orders recorded: 2
- Alerts recorded: 3
- Orphan orders: 1
- Failures: 0
