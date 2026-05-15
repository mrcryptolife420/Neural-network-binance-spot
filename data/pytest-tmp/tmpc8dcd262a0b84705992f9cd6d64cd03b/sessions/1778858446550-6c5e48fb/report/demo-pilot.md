# Demo Pilot Report 1778858446550-6c5e48fb

## Executive summary
- Mode: demo
- Symbol: BTCUSDT
- Status: running
- PnL: 0
- Max drawdown: 0
- Pilot preset: smoke
- Orders: 1 / 5
- Rejects: 0 / -
- Reconciliation: ok
- Cancel-on-stop events: 0

## Operator checklist
| check | status | detail | blocking |
| --- | --- | --- | --- |
| Profile | pass | binance-demo-spot | True |
| Credentials | pass | Credentials loaded for signed checks | True |
| Connection | pass | allowed | True |
| Server time | pass | demo base URL/gate reachable | False |
| Account canTrade | pass | ok | True |
| Clean start | pass | ok | True |
| No orphan orders | pass | 0 orphan orders | True |
| Risk limits | pass | configured | True |
| Pilot preset | pass | smoke | False |
| Armed | pass | armed | False |

## Signal to order pipeline
| step | status | timestamp_ms | detail | reference |
| --- | --- | --- | --- | --- |
| Signal | ready | - | baseline | BUY |
| Risk | allowed | - | risk ok | ALLOW |
| Intent | ready | - | BUY | 10 |
| Test order | accepted | - | ACCEPTED | demo-1 |
| Demo order | sent | - | NEW | 1001 |
| Reconciliation | ok | - | ok | 0 |
| Fill/Cancel/Reject | ok | - | ok | ok |

## Orders and reconciliation
- Orders recorded: 0
- Alerts recorded: 0
- Orphan orders: 0
- Failures: 0
