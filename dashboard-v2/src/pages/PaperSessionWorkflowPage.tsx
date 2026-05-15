import { GuidedActionCard } from "../components/guided/GuidedActionCard";

export function PaperSessionWorkflowPage() {
  return (
    <section className="panel">
      <h2>Paper Session</h2>
      <GuidedActionCard title="Start paper session" safetyLabel="paper only" command="python -m binance_spot_bot.cli paper-simulation" />
      <button className="stop-button">Stop</button>
    </section>
  );
}
