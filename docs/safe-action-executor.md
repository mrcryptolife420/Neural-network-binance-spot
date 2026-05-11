# Safe Action Executor

`ActionExecutor` runs approved proposals only.

Before execution it reloads the proposal from the queue and revalidates policy. Output is written to redacted stdout/stderr artifacts. Unapproved, expired, tampered, forbidden, live, order, or account actions are blocked.

