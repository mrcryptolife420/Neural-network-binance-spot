# Live Operations Safety Contract

Live ops tooling is an incident response, runbook, rollback drill, forensic and evidence layer.

Rules:

* Incident tooling never places live orders.
* Incident tooling never starts live sessions.
* Recovery never auto-rearms live trading.
* P0/P1 incidents keep live rearm blocked until operator review and evidence exist.
* Rollback drills run in offline fake mode by default.
* Reports redact secrets and avoid financial advice.

