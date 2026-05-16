import { useEffect, useState } from "react";
import { getJson } from "../api/client";

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function LiveTrainingPage() {
  const [health, setHealth] = useState<Record<string, unknown>>({});
  const [progress, setProgress] = useState<Record<string, unknown>>({});
  const [pipeline, setPipeline] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/live-training/health").then(setHealth).catch(() => undefined);
    getJson<Record<string, unknown>>("/api/live-training/demo-targets/progress").then(setProgress).catch(() => undefined);
  }, []);

  const runPipeline = () => {
    postJson<Record<string, unknown>>("/api/live-training/demo-to-live/run").then(setPipeline).catch(() => undefined);
  };

  return (
    <>
      <section className="panel">
        <p className="safety">DEMO-TO-LIVE TRAINING - NO LIVE TRADING</p>
        <h2>Live Training</h2>
        <p>Collect demo data, build quality evidence, validate model behavior, check testnet promotion, and keep live execution locked.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={runPipeline}>Run demo-to-live checks</button>
          <button type="button" disabled>Live start unavailable</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Health</h3>
          <pre>{JSON.stringify(health, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Demo Target Progress</h3>
          <pre>{JSON.stringify(progress, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Quality Burn-Down</h3>
          <pre>{JSON.stringify((pipeline.burndown as Record<string, unknown>) ?? {}, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Quality Gate</h3>
          <pre>{JSON.stringify((pipeline.quality as Record<string, unknown>) ?? {}, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Testnet Promotion</h3>
          <pre>{JSON.stringify((pipeline.testnet_promotion as Record<string, unknown>) ?? {}, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Live Candidate Gate</h3>
          <pre>{JSON.stringify((pipeline.live_candidate as Record<string, unknown>) ?? {}, null, 2)}</pre>
        </article>
      </section>
    </>
  );
}

