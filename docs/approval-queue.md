# Approval Queue

`ApprovalQueueStore` stores local proposals in `data/action-center/`.

Statuses include `proposed`, `needs_evidence`, `needs_confirmation`, `approved`, `rejected`, `expired`, `executing`, `executed`, `verification_failed`, `completed`, and `archived`.

The queue index includes a manifest hash and never enables live trading.

