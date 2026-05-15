# Runtime Step Pipeline

Roadmap: 095

`RuntimeStepPipeline` runs named stages against a shared context and emits `runtime.stage` events.

It does not replace `BotRuntime.step()` yet. It creates a safe extraction boundary for future stages such as market data, feature building, model signal, risk, execution preview, accounting and evidence.
