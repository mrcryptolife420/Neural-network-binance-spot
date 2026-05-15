# Pilot Acceptance 1778857058891-8a6f40de

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
| check | reason |
| --- | --- |
| credentials | api_[REDACTED] |

## Stop Gate
| no_open_orders | no_orphan_orders | reconciliation_ok | resume_required |
| --- | --- | --- | --- |
| True | True | True | False |

## Operator Checklist
| check | status | detail | blocking |
| --- | --- | --- | --- |
| Profile | pass | binance-demo-spot | True |
| Credentials | pass | loaded | True |
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
| Signal | idle | - | - | - |
| Risk | idle | - | - | - |
| Intent | idle | - | - | - |
| Test order | idle | - | - | - |
| Demo order | idle | - | - | - |
| Reconciliation | ok | - | ok | 0 |
| Fill/Cancel/Reject | ok | - | ok | ok |

## Runner
| runner_id | pid | status | last_tick_ms | last_command |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Runner Commands
_No rows._
