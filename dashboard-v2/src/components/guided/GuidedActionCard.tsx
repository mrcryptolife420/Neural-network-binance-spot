export type GuidedActionCardProps = {
  title: string;
  safetyLabel: string;
  disabledReason?: string;
  command: string;
};

export function GuidedActionCard({ title, safetyLabel, disabledReason, command }: GuidedActionCardProps) {
  return (
    <article className="guided-card">
      <h3>{title}</h3>
      <p>{safetyLabel}</p>
      <code>{command}</code>
      <button disabled={Boolean(disabledReason)}>{disabledReason ? disabledReason : "Run"}</button>
    </article>
  );
}
