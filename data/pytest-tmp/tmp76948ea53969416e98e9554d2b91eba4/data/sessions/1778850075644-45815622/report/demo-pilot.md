# Demo Pilot Report 1778850075644-45815622

## Executive summary
- Mode: paper
- Symbol: BTCUSDT
- Status: stopped
- PnL: 0.056489362345741
- Max drawdown: 0.113654929120642
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
| Test order | filled | - | FILLED | spotbot-c3ae87cc70424bd08629bda3 |
| Demo order | sent | - | FILLED | spotbot-c3ae87cc70424bd08629bda3 |
| Reconciliation | not-run | - | not-run | 0 |
| Fill/Cancel/Reject | filled | - | FILLED | FILLED |

## Orders and reconciliation
- Orders recorded: 15
- Alerts recorded: 8
- Orphan orders: 0
- Failures: 0
