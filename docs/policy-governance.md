# Policy Governance Decisions

Governance decisions are deterministic and paper-only. The decision engine accepts an experiment report, a stopping-rule report, and operator confirmation.

Allowed decisions:

- `keep_champion`
- `promote_challenger`
- `extend_experiment`
- `reduce_challenger`
- `rerun_experiment`
- `suspend_challenger`
- `archive_challenger`
- `rollback`
- `no_policy`

Promotion requires challenger leadership, enough samples, a clean stopping-rule result, and operator confirmation. Stop reports with policy violations, signed endpoint usage, or watchdog alerts suspend the challenger.
