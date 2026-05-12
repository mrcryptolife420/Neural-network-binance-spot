# Repository Knowledge Graph Safety Contract

- Analysis is local-only and read-only by default.
- Reports must be secret-free and use relative paths where possible.
- Recommendations may propose validation commands, but must not execute them automatically.
- No remote telemetry, uploads, signed endpoints, account endpoints, or order endpoints.
- Live trading enabled: false.
