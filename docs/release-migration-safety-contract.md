# Release Migration Safety Contract

Release tooling is local-only.

- No remote auto-download or telemetry.
- No live mode, signed endpoints, account endpoints, or order endpoints.
- Migration apply requires dry-run and confirmation.
- Backup gate is required for backup-gated migrations.
- Release artifacts include no-live proof and redaction proof.

