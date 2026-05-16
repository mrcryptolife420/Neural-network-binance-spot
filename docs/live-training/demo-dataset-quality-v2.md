# Demo Dataset Quality V2

The v2 quality gate scores completeness, freshness, coverage, consistency, reconciliation, market regime diversity, metadata, secret-free evidence, no-live contamination, and leakage risk.

Grades:

- `A` or `B`: eligible for validation and testnet promotion checks
- `C`: paper-only
- `D`: collect more demo data
- `F`: invalid or unsafe

Use:

```powershell
python -m binance_spot_bot.cli demo-dataset-quality-v2 --json
```
