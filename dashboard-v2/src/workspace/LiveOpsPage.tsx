import { useEffect, useState } from "react";
import { getJson } from "../api/client";

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function LiveOpsPage() {
  const [status, setStatus] = useState<Record<string, unknown>>({});
  const [incident, setIncident] = useState<Record<string, unknown>>({});
  const [drill, setDrill] = useState<Record<string, unknown>>({});
  const [recovery, setRecovery] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/live-ops/status").then(setStatus).catch(() => undefined);
  }, []);

  return (
    <>
      <section className="panel">
        <p className="safety">NO AUTOMATIC LIVE RE-ARM - OPERATOR REVIEW REQUIRED</p>
        <h2>Live Ops</h2>
        <p>Incident command center for fake-mode rollback drills, runbooks, forensics, prevention backlog and recovery readiness.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/live-ops/incidents/detect").then(setIncident)}>Detect incident</button>
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/live-ops/rollback-drills/run").then(setDrill)}>Run rollback drill</button>
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/live-ops/recovery/check").then(setRecovery)}>Recovery gate</button>
          <button type="button" disabled>Re-arm locked</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel"><h3>Status</h3><pre>{JSON.stringify(status, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Incident List</h3><pre>{JSON.stringify(incident, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Rollback Drill</h3><pre>{JSON.stringify(drill, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Recovery Gate</h3><pre>{JSON.stringify(recovery, null, 2)}</pre></article>
      </section>
    </>
  );
}

