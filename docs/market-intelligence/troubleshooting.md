# Market Intelligence Troubleshooting

Common checks:

- Run `market-intelligence-policy` if a scanner endpoint is blocked.
- Run `scanner-rate-limit-plan` before increasing watchlist size.
- Run `market-snapshot-cache-report` if local snapshots are missing.
- Run `watchlist-scan-preview` before a scan run.
- Run `dashboard-v2-market-intelligence-smoke` when Dashboard V2 routes look stale.

The scanner does not require API keys. If a flow asks for keys, it is not part of the Market Intelligence Workbench.
