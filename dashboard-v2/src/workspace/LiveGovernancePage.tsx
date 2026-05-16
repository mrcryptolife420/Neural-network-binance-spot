import { useEffect, useState } from "react";
import { getJson } from "../api/client";

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function LiveGovernancePage() {
  const [status, setStatus] = useState<Record<string, unknown>>({});
  const [review, setReview] = useState<Record<string, unknown>>({});
  const [scorecard, setScorecard] = useState<Record<string, unknown>>({});
  const [decision, setDecision] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/live-governance/status").then(setStatus).catch(() => undefined);
  }, []);

  const runReview = () => postJson<Record<string, unknown>>("/api/live-governance/review/run").then(setReview).catch(() => undefined);
  const runScorecard = () => postJson<Record<string, unknown>>("/api/live-governance/scorecards/generate").then(setScorecard).catch(() => undefined);
  const runDecision = () => postJson<Record<string, unknown>>("/api/live-governance/scaling-decision").then(setDecision).catch(() => undefined);

  return (
    <>
      <section className="panel">
        <p className="safety">NO AUTOMATIC LIVE SCALE-UP - OPERATOR APPROVAL REQUIRED</p>
        <h2>Live Governance</h2>
        <p>Review controlled sessions, generate scorecards, calibrate risk proposals, block auto-scale, and require explicit approval for lifecycle changes.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={runReview}>Run review</button>
          <button type="button" onClick={runScorecard}>Generate scorecard</button>
          <button type="button" onClick={runDecision}>Scaling decision</button>
          <button type="button" disabled>Promote locked</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel"><h3>Status</h3><pre>{JSON.stringify(status, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Session Review</h3><pre>{JSON.stringify(review, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Scorecard</h3><pre>{JSON.stringify(scorecard, null, 2)}</pre></article>
        <article className="workspace-panel"><h3>Scaling Decision</h3><pre>{JSON.stringify(decision, null, 2)}</pre></article>
      </section>
    </>
  );
}
