# Local Paper Operator Runbooks

Live trading: disabled

## Morning check

Trigger: daily_start
Severity: info

- Run health score `operator-health-score --json`
- Review local ops snapshot `local-ops-snapshot --json`

## Evening review

Trigger: daily_end
Severity: info

- Generate operator report `operator-report --json`
- Refresh evidence manifest `evidence-manifest --json`

## Failed scheduled report

Trigger: job_failed
Severity: warning

- Run diagnostics `diagnostics --json`
- Create support bundle `support-bundle --json`

## Policy challenger failed

Trigger: governance_stop
Severity: warning

- Run governance simulation `governance-simulation --case policy_violation --json`
- Write weekly governance report `weekly-governance-report --json`

## Browser smoke failed

Trigger: dashboard_smoke_failed
Severity: warning

- Run dashboard smoke `dashboard-smoke --seconds 1`
- Create support bundle `support-bundle --json`
