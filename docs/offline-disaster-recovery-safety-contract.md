# Offline Disaster Recovery Safety Contract

Roadmap: 088

Backup and restore flows are offline, local, redacted, preview-first, and no-live. Forbidden files such as `.env`, `.pem`, and `.key` are excluded from safe backups.

Restore execution remains blocked unless an explicit offline restore confirmation is supplied, and preview reports are the default behavior.
