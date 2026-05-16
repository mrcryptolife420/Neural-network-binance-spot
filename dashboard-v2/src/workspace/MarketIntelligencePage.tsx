import { useEffect, useState } from "react";
import { getJson } from "../api/client";

type ScannerPreset = {
  preset_id: string;
  symbols: string[];
  ranking_dimension: string;
};

type RankRow = {
  rank: number;
  symbol: string;
  value: string | number;
};

type ScanMetric = {
  symbol: string;
  last_price: string;
  quote_volume_24h: string;
  spread_bps: string;
  intraday_volatility: string;
  data_quality_score: string;
};

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function MarketIntelligencePage() {
  const [presets, setPresets] = useState<ScannerPreset[]>([]);
  const [selected, setSelected] = useState("majors_overview");
  const [policy, setPolicy] = useState<Record<string, unknown>>({});
  const [plan, setPlan] = useState<Record<string, unknown>>({});
  const [scan, setScan] = useState<{ metrics?: ScanMetric[]; run_id?: string }>({});
  const [ranking, setRanking] = useState<{ ranks?: RankRow[] }>({});
  const [paper, setPaper] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<{ presets: ScannerPreset[] }>("/api/market-intelligence/scanner-presets")
      .then((payload) => {
        setPresets(payload.presets);
        if (payload.presets[0]) setSelected(payload.presets[0].preset_id);
      })
      .catch(() => undefined);
    getJson<Record<string, unknown>>("/api/market-intelligence/policy").then(setPolicy).catch(() => undefined);
  }, []);

  const preview = () => {
    postJson<Record<string, unknown>>(`/api/market-intelligence/scan/preview?preset=${selected}`).then(setPlan).catch(() => undefined);
  };

  const runScan = () => {
    postJson<{ metrics?: ScanMetric[]; run_id?: string }>(`/api/market-intelligence/scan/run?preset=${selected}`)
      .then((payload) => {
        setScan(payload);
        return getJson<{ ranks?: RankRow[] }>(`/api/market-intelligence/rankings/${payload.run_id ?? "latest"}`);
      })
      .then(setRanking)
      .catch(() => undefined);
  };

  const previewPaper = () => {
    postJson<Record<string, unknown>>("/api/market-intelligence/paper-analytics/preview").then(setPaper).catch(() => undefined);
  };

  return (
    <>
      <section className="panel">
        <p className="safety">MARKET INTELLIGENCE - NO LIVE TRADING</p>
        <h2>Market Intelligence Workbench</h2>
        <p>Public unsigned Binance Spot market data only. Rankings are local research metrics and not financial advice.</p>
        <div className="workspace-toolbar">
          <label>
            Preset
            <select value={selected} onChange={(event) => setSelected(event.target.value)}>
              {presets.map((preset) => (
                <option key={preset.preset_id} value={preset.preset_id}>{preset.preset_id}</option>
              ))}
            </select>
          </label>
          <button type="button" onClick={preview}>Preview budget</button>
          <button type="button" onClick={runScan}>Run public scan</button>
          <button type="button" onClick={previewPaper}>Paper analytics</button>
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Public Policy</h3>
          <pre>{JSON.stringify(policy, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Rate Budget</h3>
          <pre>{JSON.stringify(plan, null, 2)}</pre>
        </article>
      </section>
      <section className="panel">
        <h2>Scanner Metrics</h2>
        <div className="market-table">
          <div className="market-row market-head"><span>Symbol</span><span>Last</span><span>Volume</span><span>Spread bps</span><span>Volatility</span><span>Quality</span></div>
          {(scan.metrics ?? []).map((metric) => (
            <div className="market-row" key={metric.symbol}>
              <span>{metric.symbol}</span>
              <span>{metric.last_price}</span>
              <span>{metric.quote_volume_24h}</span>
              <span>{metric.spread_bps}</span>
              <span>{metric.intraday_volatility}</span>
              <span>{metric.data_quality_score}</span>
            </div>
          ))}
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Rankings</h3>
          <ol>
            {(ranking.ranks ?? []).map((row) => (
              <li key={`${row.rank}-${row.symbol}`}>{row.symbol}: {row.value}</li>
            ))}
          </ol>
        </article>
        <article className="workspace-panel">
          <h3>Paper Analytics</h3>
          <pre>{JSON.stringify(paper, null, 2)}</pre>
        </article>
      </section>
    </>
  );
}
