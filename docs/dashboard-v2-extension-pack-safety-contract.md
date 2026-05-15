# Dashboard V2 Extension Pack Safety Contract

Dashboard V2 extension packs are pluginless, local-only JSON/Markdown metadata bundles.

Rules:

- No arbitrary JavaScript, Python, eval, scripts or function bodies.
- No remote marketplace, cloud sync, remote downloads or telemetry.
- No live mode, signed order actions, account actions or live trading controls.
- Packs may only reference allowlisted Dashboard V2 widgets.
- Workspace templates must keep `no_live_banner` and `stop_button`.
- Import is preview-first and install requires explicit local confirmation.
- Export and evidence are redacted and include `live_trading_enabled=false`.
