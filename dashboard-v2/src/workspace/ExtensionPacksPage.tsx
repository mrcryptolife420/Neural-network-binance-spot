import { useEffect, useState } from "react";
import { getJson } from "../api/client";

type PackManifest = {
  pack_id: string;
  name: string;
  description: string;
  pack_type: string;
  version: string;
  live_trading_enabled: false;
};

export function ExtensionPacksPage() {
  const [packs, setPacks] = useState<PackManifest[]>([]);
  const [recommendation, setRecommendation] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<{ packs: PackManifest[] }>("/api/extension-packs").then((payload) => setPacks(payload.packs)).catch(() => undefined);
    getJson<Record<string, unknown>>("/api/extension-packs/recommendations").then(setRecommendation).catch(() => undefined);
  }, []);

  return (
    <>
      <section className="panel">
        <p className="safety">LOCAL REALTIME DASHBOARD - NO LIVE TRADING</p>
        <h2>Extension Packs</h2>
        <p>Local pluginless packs only. No code execution, no cloud marketplace, no live trading.</p>
      </section>
      <section className="pack-grid">
        {packs.map((pack) => (
          <article key={pack.pack_id} className="workspace-panel">
            <h3>{pack.name}</h3>
            <p>{pack.description}</p>
            <dl className="metrics">
              <div><dt>Type</dt><dd>{pack.pack_type}</dd></div>
              <div><dt>Version</dt><dd>{pack.version}</dd></div>
            </dl>
            <button type="button">Preview install</button>
          </article>
        ))}
      </section>
      <section className="panel">
        <h2>Recommendation</h2>
        <pre>{JSON.stringify(recommendation, null, 2)}</pre>
      </section>
    </>
  );
}
