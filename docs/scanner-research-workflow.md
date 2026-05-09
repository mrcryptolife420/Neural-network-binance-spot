# Scanner research workflow

The scanner is read-only research infrastructure.

Dashboard Research tab:

- ranks watchlist symbols by spread, volume, signal and confidence;
- records scanner runs in `ScannerHistory`;
- indexes runs in `ExperimentDB`;
- exports local HTML and notebook reports;
- never creates order intents.

All scanner output is local and redacted before export. Scanner results are research signals only; execution remains gated by deterministic risk and paper/testnet-readiness flows.
