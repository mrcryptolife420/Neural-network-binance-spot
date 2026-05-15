# Pilot Acceptance 1778866526258-cac989ae

- Final acceptance: accepted
- Mode: demo
- Symbol: BTCUSDT
- Status: running
- Stop final state: completed
- Orders: 0
- Alerts: 0
- Runner status: -
- Runner id: -

## Start Gate
_No rows._

## Stop Gate
| no_open_orders | no_orphan_orders | reconciliation_ok | resume_required |
| --- | --- | --- | --- |
| True | True | True | False |

## Operator Checklist
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

## Pipeline
| step | status | timestamp_ms | detail | reference |
| --- | --- | --- | --- | --- |
| Signal | ready | - | baseline | BUY |
| Risk | allowed | - | risk ok | ALLOW |
| Intent | ready | - | BUY | 10 |
| Test order | accepted | - | ACCEPTED | demo-1 |
| Demo order | sent | - | NEW | 1001 |
| Reconciliation | ok | - | ok | 0 |
| Fill/Cancel/Reject | ok | - | ok | ok |

## Runner
| runner_id | pid | status | last_tick_ms | last_command |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Runner Commands
_No rows._
