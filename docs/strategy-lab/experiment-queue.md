# Experiment Queue

Strategy Lab queues contain deterministic paper-only jobs.

Each job records symbol, interval, data source, strategy id, model alias, risk preset, seed, max steps, starting quote, expected artifacts, blockers, and safe status.

Queue validation blocks duplicate jobs, unsupported strategies, unsupported model aliases, unsupported risk presets, unsupported data sources, and live-enabled jobs.
