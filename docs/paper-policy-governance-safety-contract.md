# Paper Policy Governance Safety Contract

Roadmap: 082

Policy governance is local paper-only. It may register portfolio policies, compare champion/challenger variants, write rollout reports, export evidence bundles, and produce rollback decisions for paper policy metadata.

It must not place orders, call signed Binance endpoints, read account balances, enable live trading, or store secrets. Promotion means `champion` inside the local paper policy registry only. Rollback means reverting local paper metadata to a previous champion or conservative no-trade policy.

Required operator confirmations:

- `PAPER_POLICY_PROMOTE` for paper champion promotion.
- `PAPER_POLICY_ROLLOUT` for higher-risk paper rollout stages.
- `PAPER_AB` for starting an A/B paper experiment.
- `PAPER_POLICY_ROLLBACK` for rollback.

Evidence outputs are written under `data/policy-governance/` and are redacted before persistence.
