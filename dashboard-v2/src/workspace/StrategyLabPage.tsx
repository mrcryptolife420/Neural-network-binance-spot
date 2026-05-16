import { useEffect, useState } from "react";
import { getJson } from "../api/client";

type Candidate = {
  candidate_id: string;
  symbol: string;
  data_quality_status: string;
  ranking_reasons: string[];
};

type JobResult = {
  job_id: string;
  symbol: string;
  paper_pnl: string;
  max_drawdown: string;
  status: string;
};

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function StrategyLabPage() {
  const [health, setHealth] = useState<Record<string, unknown>>({});
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [queuePreview, setQueuePreview] = useState<Record<string, unknown>>({});
  const [results, setResults] = useState<JobResult[]>([]);
  const [comparison, setComparison] = useState<Record<string, unknown>>({});
  const [scorecards, setScorecards] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/strategy-lab/health").then(setHealth).catch(() => undefined);
    postJson<{ candidates: Candidate[] }>("/api/strategy-lab/candidates/build").then((payload) => setCandidates(payload.candidates)).catch(() => undefined);
    getJson<{ results: JobResult[] }>("/api/strategy-lab/results").then((payload) => setResults(payload.results)).catch(() => undefined);
  }, []);

  const previewQueue = () => {
    postJson<Record<string, unknown>>("/api/strategy-lab/queue/preview?preset=small_safe_smoke").then(setQueuePreview).catch(() => undefined);
  };

  const loadComparison = () => {
    postJson<Record<string, unknown>>("/api/strategy-lab/comparison").then(setComparison).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/strategy-lab/scorecards").then(setScorecards).catch(() => undefined);
  };

  return (
    <>
      <section className="panel">
        <p className="safety">STRATEGY LAB - PAPER ONLY - NO LIVE TRADING</p>
        <h2>Strategy Lab</h2>
        <p>Scanner candidates become local paper-only experiment queues. No live trading, no account endpoints, no order endpoints.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={previewQueue}>Preview queue</button>
          <button type="button" onClick={loadComparison}>Load comparison</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Health</h3>
          <pre>{JSON.stringify(health, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Queue Preview</h3>
          <pre>{JSON.stringify(queuePreview, null, 2)}</pre>
        </article>
      </section>
      <section className="panel">
        <h2>Candidates</h2>
        <div className="market-table">
          <div className="market-row market-head"><span>Symbol</span><span>Quality</span><span>Reasons</span><span>Candidate</span><span>Mode</span><span>Status</span></div>
          {candidates.map((candidate) => (
            <div className="market-row" key={candidate.candidate_id}>
              <span>{candidate.symbol}</span>
              <span>{candidate.data_quality_status}</span>
              <span>{candidate.ranking_reasons.join(", ")}</span>
              <span>{candidate.candidate_id}</span>
              <span>paper</span>
              <span>research</span>
            </div>
          ))}
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Results</h3>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Comparison</h3>
          <pre>{JSON.stringify(comparison, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Scorecards</h3>
          <pre>{JSON.stringify(scorecards, null, 2)}</pre>
        </article>
      </section>
    </>
  );
}
