# Action Policy Validator

`ActionPolicy` validates proposals before queueing, approval, and execution.

It blocks unknown commands, shell injection tokens, secret-like arguments, live mode, signed/order/account endpoints, output paths outside the data directory, missing required evidence, destructive actions without preview evidence, and paper risk changes without governance evidence.

