# Local Job Schema

Local jobs are represented by `LocalJobDefinition`, `LocalJobSchedule`, `LocalJobRun`, `LocalJobResult`, `LocalJobAllowlistRule`, and `LocalJobFailurePolicy`.

Definitions include job id, command, args, category, schedule, max runtime, retry policy, failure policy, output directory, enabled state, timestamps, and `live_trading_enabled: false`.

Jobs are JSON serializable and stored locally under `data/local-jobs/`.
