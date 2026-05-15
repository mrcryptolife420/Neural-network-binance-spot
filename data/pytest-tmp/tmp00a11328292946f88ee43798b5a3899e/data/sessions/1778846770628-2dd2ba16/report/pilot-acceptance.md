# Pilot Acceptance 1778846770628-2dd2ba16

- Final acceptance: accepted
- Mode: demo
- Symbol: BTCUSDT
- Status: stopped
- Stop final state: completed
- Orders: 1
- Alerts: 4
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

## Pipeline
| step | status | timestamp_ms | detail | reference |
| --- | --- | --- | --- | --- |
| Signal | idle | - | - | - |
| Risk | idle | - | - | - |
| Intent | idle | - | - | - |
| Test order | idle | - | - | - |
| Demo order | idle | - | - | - |
| Reconciliation | not-run | - | not-run | 0 |
| Fill/Cancel/Reject | not-run | - | - | not-run |

## Runner
| runner_id | pid | status | last_tick_ms | last_command |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Runner Commands
_No rows._
