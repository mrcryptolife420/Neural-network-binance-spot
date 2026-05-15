import { GuidedActionCard } from "../components/guided/GuidedActionCard";
import { SafetyPrecheck } from "../components/guided/SafetyPrecheck";

export function DemoSpotWizardPage() {
  return (
    <section className="panel">
      <h2>Demo Spot</h2>
      <SafetyPrecheck />
      <GuidedActionCard title="Preview demo order" safetyLabel="demo only" command="python -m binance_spot_bot.cli demo-execution-preview" />
    </section>
  );
}
