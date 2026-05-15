# Demo Pilot Report 1778846004270-e2e33330

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
| Test order | filled | - | FILLED | spotbot-4de560ae04844cfdb65d578f |
| Demo order | sent | - | FILLED | spotbot-4de560ae04844cfdb65d578f |
| Reconciliation | not-run | - | not-run | 0 |
| Fill/Cancel/Reject | filled | - | FILLED | FILLED |

## Orders and reconciliation
- Orders recorded: 15
- Alerts recorded: 8
- Orphan orders: 0
- Failures: 0
