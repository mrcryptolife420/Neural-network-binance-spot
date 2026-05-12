# Offline Disaster Recovery Safety Contract

Disaster recovery is local-only and offline.

- Backups exclude environment files, private key files, credential files, and path traversal.
- Restore is preview-first by default.
- Controlled restore requires `RESTORE_OFFLINE_STATE`.
- Backup and restore never call Binance, signed endpoints, order endpoints, or account endpoints.
- Every backup includes no-live proof, redaction proof, manifest data, and hashes.

