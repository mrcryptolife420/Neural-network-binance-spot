# Pilot Acceptance 1778851232178-5569dce1

- Final acceptance: accepted
- Mode: demo
- Symbol: BTCUSDT
- Status: stopped
- Stop final state: completed
- Orders: 3
- Alerts: 2
- Runner status: -
- Runner id: -

## Start Gate
| check | status | reason | next_action | blocking |
| --- | --- | --- | --- | --- |
| profile | pass | binance-demo-spot | Select Binance Demo Spot profile | True |
| demo_base_url | pass | https://demo-api.binance.com | Use Demo Spot base URL | True |
| live_disabled | pass | live disabled | Disable live trading | True |
| credentials | pass | Credentials loaded for signed checks | Load Demo Spot credentials | True |
| connection | pass | allowed | Test connection | True |
| account_can_trade | pass | ok | Sync Demo Spot account | True |
| filters_loaded | pass | symbol filters ready | Refresh symbol filters | True |
| risk_limits | pass | configured | Set risk limits | True |
| pilot_preset | pass | smoke | Choose pilot preset | True |
| armed | pass | armed | Arm Demo Spot trading | True |
| clean_start | pass | ok | Reconcile/cancel before start | True |
| no_open_orders | pass | 0 open orders | Cancel or reconcile open orders | True |
| runtime_idle | pass | running | Stop current runtime | True |

## Stop Gate
| no_open_orders | no_orphan_orders | reconciliation_ok | resume_required |
| --- | --- | --- | --- |
| True | True | False | False |

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
| Pilot preset | warn | not selected | False |
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
