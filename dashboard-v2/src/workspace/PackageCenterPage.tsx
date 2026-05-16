import { useEffect, useState } from "react";
import { getJson } from "../api/client";

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function PackageCenterPage() {
  const [status, setStatus] = useState<Record<string, unknown>>({});
  const [backup, setBackup] = useState<Record<string, unknown>>({});
  const [update, setUpdate] = useState<Record<string, unknown>>({});
  const [evidence, setEvidence] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/package/status").then(setStatus).catch(() => undefined);
  }, []);

  return (
    <>
      <section className="panel">
        <p className="safety">PACKAGING NEVER AUTO-STARTS LIVE TRADING</p>
        <h2>Package Center</h2>
        <p>Local installer, portable bundle, startup health, safe update guard, backup, rollback and offline recovery kit.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/package/backup/create").then(setBackup)}>Create backup</button>
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/package/update/plan").then(setUpdate)}>Update guard</button>
          <button type="button" onClick={() => postJson<Record<string, unknown>>("/api/package/evidence/export").then(setEvidence)}>Export evidence</button>
          <button type="button" disabled>Live start locked</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel"><h3>Package Status</h3><pre>{JSON.stringify(status, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Backup Restore</h3><pre>{JSON.stringify(backup, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Update Guard</h3><pre>{JSON.stringify(update, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Package Evidence</h3><pre>{JSON.stringify(evidence, null, 2)}</pre></article>
      </section>
    </>
  );
}

