import { useEffect, useState } from "react";
import { getJson } from "../api/client";

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function AIDoctorPage() {
  const [status, setStatus] = useState<Record<string, unknown>>({});
  const [summary, setSummary] = useState<Record<string, unknown>>({});
  const [prompt, setPrompt] = useState<Record<string, unknown>>({});
  const [bundle, setBundle] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/ai-doctor/status").then(setStatus).catch(() => undefined);
  }, []);

  return (
    <>
      <section className="panel">
        <p className="safety">AI DOCTOR NEVER PLACES ORDERS OR STARTS LIVE SESSIONS</p>
        <h2>AI Doctor</h2>
        <p>Local debug bundle, known issue matching, AI summary and Codex fix prompt generator.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/ai-doctor/runs/latest/summary").then(setSummary)}>Generate summary</button>
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/ai-doctor/runs/latest/codex-prompt").then(setPrompt)}>Codex prompt</button>
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/ai-doctor/runs/latest/export").then(setBundle)}>Export AI Doctor Bundle</button>
          <button type="button" disabled>Live controls locked</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel"><h3>Current Run</h3><pre>{JSON.stringify(status, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Known Issue Matches</h3><pre>{JSON.stringify(summary, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Codex Fix Prompt</h3><pre>{JSON.stringify(prompt, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Debug Bundle</h3><pre>{JSON.stringify(bundle, null, 2)}</pre></article>
      </section>
    </>
  );
}

