# Local Job Allowlist

The allowlist accepts local diagnostics, report, evidence, governance, smoke, and cleanup-preview commands. It blocks unknown commands, live mode, order/account/signed commands, shell injection tokens, and secret-like arguments.

Examples allowed:

- `operator-report --json`
- `operator-health-score --json`
- `weekly-governance-report --json`

Examples blocked:

- `demo-execution-place --armed`
- `paper-session --mode live`
- commands containing `;`, `|`, redirection, signatures, or API keys
