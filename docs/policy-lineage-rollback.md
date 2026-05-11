# Policy Lineage And Rollback

The portfolio policy registry stores policy metadata, decisions, latest champion alias, and lineage events. Champion promotion archives the previous champion and writes the previous champion ID onto the new champion.

Rollback requires the exact confirmation string `PAPER_POLICY_ROLLBACK`. A rollback promotes the previous champion through the same registry path and records the decision as local paper governance evidence.

Rollback never enables live trading and never places orders.
