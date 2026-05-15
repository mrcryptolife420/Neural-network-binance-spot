# Local Paper Ops Runbook

All jobs are local paper/demo jobs. Live trading stays disabled.

- morning-quality-gate: `spot-bot operator-quality-gate --json` - Check before demo trading.
- evening-operator-report: `spot-bot operator-report --json` - Review paper health and incidents.
- weekly-support-verify: `spot-bot support-bundles-verify --json` - Verify bundle restore safety.
- weekly-evidence-chain: `spot-bot evidence-chain --json` - Check evidence integrity chain.