import { useEffect, useState } from "react";
import { getJson } from "../api/client";

type BasketItem = {
  item_id: string;
  symbol: string;
  paper_score: number;
  data_quality_score: number;
  market_quality_score: number;
};

type EquityPoint = {
  step: number;
  equity: number;
  drawdown: number;
};

async function postJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { method: "POST" });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json() as Promise<T>;
}

export function PortfolioLabPage() {
  const [health, setHealth] = useState<Record<string, unknown>>({});
  const [basket, setBasket] = useState<Record<string, unknown>>({});
  const [allocation, setAllocation] = useState<Record<string, unknown>>({});
  const [preview, setPreview] = useState<Record<string, unknown>>({});
  const [guards, setGuards] = useState<Record<string, unknown>>({});
  const [scorecards, setScorecards] = useState<Record<string, unknown>>({});
  const [stress, setStress] = useState<Record<string, unknown>>({});
  const [robustness, setRobustness] = useState<Record<string, unknown>>({});
  const [coverage, setCoverage] = useState<Record<string, unknown>>({});
  const [performance, setPerformance] = useState<Record<string, unknown>>({});
  const [gate, setGate] = useState<Record<string, unknown>>({});

  useEffect(() => {
    getJson<Record<string, unknown>>("/api/portfolio-lab/health").then(setHealth).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/baskets/build").then(setBasket).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/allocations/propose?mode=equal_weight").then(setAllocation).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/simulations/preview").then(setPreview).catch(() => undefined);
  }, []);

  const loadResearch = () => {
    postJson<Record<string, unknown>>("/api/portfolio-lab/stress-tests/run").then(setStress).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/scorecards").then(setScorecards).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/research-guards").then(setGuards).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/rolling-simulation/preview").then(setRobustness).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/dataset-coverage/audit").then(setCoverage).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/walk-forward/performance").then(setPerformance).catch(() => undefined);
    postJson<Record<string, unknown>>("/api/portfolio-lab/robustness/governance-gate").then(setGate).catch(() => undefined);
  };

  const isRobustness = window.location.pathname.includes("robustness") || window.location.pathname.includes("walk-forward");
  const basketItems = (((basket.basket as Record<string, unknown> | undefined)?.items ?? []) as BasketItem[]);
  const previewBasket = preview.basket as Record<string, unknown> | undefined;
  const equityCurve = (((preview as Record<string, unknown>).simulation as Record<string, unknown> | undefined)?.equity_curve ?? []) as EquityPoint[];

  return (
    <>
      <section className="panel">
        <p className="safety">PORTFOLIO LAB - PAPER ONLY - NO LIVE TRADING</p>
        <h2>Portfolio Lab</h2>
        <p>Local paper-only basket research for Strategy Lab candidates. No account endpoints, no order endpoints, no real allocation.</p>
        <div className="workspace-toolbar">
          <button type="button" onClick={loadResearch}>Load research checks</button>
        </div>
      </section>
      {isRobustness && (
        <section className="pack-grid">
          <article className="workspace-panel">
            <h3>Walk-Forward Split</h3>
            <pre>{JSON.stringify(robustness, null, 2)}</pre>
          </article>
          <article className="workspace-panel">
            <h3>Dataset Coverage</h3>
            <pre>{JSON.stringify(coverage, null, 2)}</pre>
          </article>
          <article className="workspace-panel">
            <h3>Walk-Forward Performance</h3>
            <pre>{JSON.stringify(performance, null, 2)}</pre>
          </article>
          <article className="workspace-panel">
            <h3>Governance Gate</h3>
            <pre>{JSON.stringify(gate, null, 2)}</pre>
          </article>
        </section>
      )}
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Health</h3>
          <pre>{JSON.stringify(health, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Allocation Preview</h3>
          <pre>{JSON.stringify(allocation, null, 2)}</pre>
        </article>
      </section>
      <section className="panel">
        <h2>Candidate Basket</h2>
        <div className="market-table">
          <div className="market-row market-head"><span>Symbol</span><span>Paper score</span><span>Data quality</span><span>Market quality</span><span>Mode</span><span>Status</span></div>
          {basketItems.map((item) => (
            <div className="market-row" key={item.item_id}>
              <span>{item.symbol}</span>
              <span>{item.paper_score}</span>
              <span>{item.data_quality_score}</span>
              <span>{item.market_quality_score}</span>
              <span>paper</span>
              <span>research</span>
            </div>
          ))}
        </div>
      </section>
      <section className="pack-grid">
        <article className="workspace-panel">
          <h3>Simulation Preview</h3>
          <pre>{JSON.stringify(previewBasket ?? preview, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Stress Tests</h3>
          <pre>{JSON.stringify(stress, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Scorecards</h3>
          <pre>{JSON.stringify(scorecards, null, 2)}</pre>
        </article>
        <article className="workspace-panel">
          <h3>Research Guards</h3>
          <pre>{JSON.stringify(guards, null, 2)}</pre>
        </article>
      </section>
      <section className="panel">
        <h2>Portfolio Equity Curve</h2>
        <div className="mini-chart" aria-label="portfolio equity chart">
          {(equityCurve.length ? equityCurve : [{ step: 0, equity: 1000, drawdown: 0 }]).slice(-24).map((point) => (
            <span
              key={point.step}
              style={{ height: `${Math.max(8, Math.min(96, (point.equity / 1020) * 80))}%` }}
              title={`Step ${point.step}: ${point.equity}`}
            />
          ))}
        </div>
      </section>
    </>
  );
}
