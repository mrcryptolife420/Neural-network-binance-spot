# Demo Pilot Report 1778845682758-3fccad1a

## Executive summary
- Mode: demo
- Symbol: BTCUSDT
- Status: stopped
- PnL: 0.094787080659011437562438
- Max drawdown: 0.7194570267105500199800200
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
| Test order | filled | - | FILLED | spotbot-90f15824ef62479aa2171abb |
| Demo order | sent | - | FILLED | spotbot-90f15824ef62479aa2171abb |
| Reconciliation | not-run | - | not-run | 0 |
| Fill/Cancel/Reject | filled | - | FILLED | FILLED |

## Orders and reconciliation
- Orders recorded: 25
- Alerts recorded: 10
- Orphan orders: 0
- Failures: 0
