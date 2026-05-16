# Multi-Symbol Strategy Lab Safety Contract

Roadmap 113 adds a local strategy lab above the Market Intelligence scanner.

Rules:

- Experiments are paper-only.
- Live trading remains disabled.
- Signed, account, user-data, order, cancel, and listen-key endpoints are forbidden.
- API keys are not required.
- Scanner rankings are research inputs only.
- Candidate scorecards are research scorecards, not financial advice.
- Queue runs require `RUN_PAPER_EXPERIMENTS_ONLY`.
- Reports and evidence must be redacted before writing to disk.

Validation commands:

```powershell
python -m binance_spot_bot.cli strategy-lab-candidates-build --json
python -m binance_spot_bot.cli strategy-lab-queue-preview --json
python -m binance_spot_bot.cli dashboard-v2-strategy-lab-smoke --json
```
