# Dataset Quality Burn-Down

The burn-down report turns missing targets and vault blockers into actionable data quality issues.

Priority classes:

- `DQ-P0`: secret leak, live contamination, or safety failure
- `DQ-P1`: missing critical training data
- `DQ-P2`: validation coverage weakness
- `DQ-P3`: quality improvement
- `DQ-P4`: polish

Use:

```powershell
python -m binance_spot_bot.cli demo-dataset-burndown --json
```
