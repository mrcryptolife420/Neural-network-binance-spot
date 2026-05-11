# Local Scheduler

The local scheduler loads job definitions from `data/local-jobs/jobs.json`, finds due jobs with a fake-clock friendly scheduler, and can run in dry-run or one-shot tick mode.

It uses a local lock file to prevent duplicate scheduler ticks. Dry-run mode reports due jobs without executing anything.
