import { useEffect, useState } from "react";
import { getJson } from "../api/client";

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function LiveSafetyPage() {
  const [status, setStatus] = useState<Record<string, unknown>>({});
  const [dryRun, setDryRun] = useState<Record<string, unknown>>({});
  const [preview, setPreview] = useState<Record<string, unknown>>({});
  const [drill, setDrill] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/live/status").then(setStatus).catch(() => undefined);
  }, []);

  const runDryRun = () => postJson<Record<string, unknown>>("/api/live/dry-run/start").then(setDryRun).catch(() => undefined);
  const buildPreview = () => postJson<Record<string, unknown>>("/api/live/order-preview").then(setPreview).catch(() => undefined);
  const runKillSwitch = () => postJson<Record<string, unknown>>("/api/live/safety-drills/kill-switch").then(setDrill).catch(() => undefined);

  return (
    <>
      <section className="panel">
        <p className="safety">NO AUTO LIVE START - MANUAL GATED LIVE SAFETY ONLY</p>
        <h2>Live Safety</h2>
        <p>Run read-only checks, dry-run validation, order preview, sizing guards, drills, audit evidence, and keep first-order execution blocked until every gate is explicit.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={runDryRun}>Run dry-run</button>
          <button type="button" onClick={buildPreview}>Build preview</button>
          <button type="button" onClick={runKillSwitch}>Kill-switch drill</button>
          <button type="button" disabled>First real order locked</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Live Locked Status</h3>
          <pre>{JSON.stringify(status, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Dry-Run Timeline</h3>
          <pre>{JSON.stringify(dryRun, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Order Preview</h3>
          <pre>{JSON.stringify(preview, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Emergency Stop Drill</h3>
          <pre>{JSON.stringify(drill, null, 2)}</pre>
        </article>
      </section>
    </>
  );
}
