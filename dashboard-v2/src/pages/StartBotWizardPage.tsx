import { GuidedChecklist } from "../components/guided/GuidedChecklist";
import { SafetyPrecheck } from "../components/guided/SafetyPrecheck";

export function StartBotWizardPage() {
  return (
    <section className="panel">
      <h2>Start Bot</h2>
      <SafetyPrecheck />
      <GuidedChecklist items={["Mode: demo/paper/testnet-readiness", "Source", "Symbol", "Risk preset", "Start"]} />
    </section>
  );
}
