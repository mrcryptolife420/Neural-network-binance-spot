import { useEffect, useState } from "react";
import { getJson } from "../api/client";

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function LiveSessionPage() {
  const [status, setStatus] = useState<Record<string, unknown>>({});
  const [budget, setBudget] = useState<Record<string, unknown>>({});
  const [heartbeat, setHeartbeat] = useState<Record<string, unknown>>({});
  const [reconciliation, setReconciliation] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/live-session/status").then(setStatus).catch(() => undefined);
    getJson<Record<string, unknown>>("/api/live-session/budget").then(setBudget).catch(() => undefined);
    getJson<Record<string, unknown>>("/api/live-session/heartbeat").then(setHeartbeat).catch(() => undefined);
  }, []);

  const reconcile = () => postJson<Record<string, unknown>>("/api/live-session/orders/reconcile").then(setReconciliation).catch(() => undefined);

  return (
    <>
      <section className="panel">
        <p className="safety">NO UNATTENDED LIVE TRADING - CONTROLLED SESSION ONLY</p>
        <h2>Live Session</h2>
        <p>Plan controlled micro-live sessions, enforce budgets, require reconciliation after every order, monitor heartbeat, and disarm automatically on hard risk triggers.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={reconcile}>Run reconciliation</button>
          <button type="button" disabled>Arm requires manual confirmation</button>
          <button type="button">Emergency stop</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Session Status</h3>
          <pre>{JSON.stringify(status, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Budget Remaining</h3>
          <pre>{JSON.stringify(budget, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Heartbeat</h3>
          <pre>{JSON.stringify(heartbeat, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Reconciliation</h3>
          <pre>{JSON.stringify(reconciliation, null, 2)}</pre>
        </article>
      </section>
    </>
  );
}
