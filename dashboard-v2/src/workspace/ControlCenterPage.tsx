import { useEffect, useState } from "react";
import { getJson } from "../api/client";

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function ControlCenterPage() {
  const [health, setHealth] = useState<Record<string, unknown>>({});
  const [profiles, setProfiles] = useState<Record<string, unknown>>({});
  const [wizard, setWizard] = useState<Record<string, unknown>>({});
  const [runtime, setRuntime] = useState<Record<string, unknown>>({});
  const [training, setTraining] = useState<Record<string, unknown>>({});
  const [readiness, setReadiness] = useState<Record<string, unknown>>({});
  const [matrix, setMatrix] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/app-control/health").then(setHealth).catch(() => undefined);
    getJson<Record<string, unknown>>("/api/app-control/profiles").then(setProfiles).catch(() => undefined);
    getJson<Record<string, unknown>>("/api/app-control/profile-matrix").then(setMatrix).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/app-control/config-wizard/profile?profile_type=paper&symbol=BTCUSDT").then(setWizard).catch(() => undefined);
  }, []);

  const startPaper = () => {
    postJson<Record<string, unknown>>("/api/app-control/runtime/start?profile_type=paper").then(setRuntime).catch(() => undefined);
  };

  const loadTraining = () => {
    postJson<Record<string, unknown>>("/api/live-training/model-validation-gate").then(setTraining).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/app-control/live-readiness").then(setReadiness).catch(() => undefined);
  };

  return (
    <>
      <section className="panel">
        <p className="safety">ONE-CLICK LAUNCHER NEVER AUTO-STARTS LIVE TRADING</p>
        <h2>Control Center</h2>
        <p>Choose a safe profile, start local paper/demo flows, record demo training evidence, and keep live locked behind readiness gates.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={startPaper}>Start paper profile</button>
          <button type="button" onClick={loadTraining}>Load training gates</button>
          <button type="button" disabled>Kill switch visible</button>
          <button type="button" disabled>Stop always visible</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Startup Health</h3>
          <pre>{JSON.stringify(health, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Profile Wizard</h3>
          <pre>{JSON.stringify(wizard, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Runtime</h3>
          <pre>{JSON.stringify(runtime, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Live Readiness</h3>
          <pre>{JSON.stringify(readiness, null, 2)}</pre>
        </article>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Profiles</h3>
          <pre>{JSON.stringify(profiles, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Demo Training Validation</h3>
          <pre>{JSON.stringify(training, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Profile Matrix</h3>
          <pre>{JSON.stringify(matrix, null, 2)}</pre>
        </article>
      </section>
    </>
  );
}

