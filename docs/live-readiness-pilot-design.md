# Live-readiness pilot design

Status: design only. Live trading remains disabled.

## Evidence gate

- `check-all` must pass.
- Secret scan must have zero findings.
- Paper reports must show reconciliation, kill switch, and max-loss behavior.
- Shadow mode must prove no signed order endpoint is called.
- Manual approval is required outside the app before any future pilot.

## Account safety checklist

- Withdrawal permissions disabled.
- IP restrictions enabled where possible.
- Separate keys for read-only, user-data, and trade test flows.
- Small notional limits.
- Emergency stop tested before any pilot.

## No-go criteria

- Any unresolved order.
- Any stale data critical alert.
- Any missing session report.
- Any secret found in repository, logs, reports, or support bundles.
- Any path that can enable live mode from dashboard or CLI.

## Pilot simulation report

Run only as shadow mode plus testnet/demo paper accounting. The report must include evidence hashes, preflight, check-all output, session report, and rollback/kill-switch proof.

Roadmap 015 evidence additions:

- long-running paper session report bundle;
- alert and order lifecycle artifacts;
- replay/compare evidence;
- scanner research export proof;
- readiness score evidence record.

These artifacts are still not live approval. They only support a later manual audit.
