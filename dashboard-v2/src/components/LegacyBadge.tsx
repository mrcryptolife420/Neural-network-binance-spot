export function LegacyBadge({ reason }: { reason: string }) {
  return <span className="legacy">Legacy fallback: {reason}</span>;
}
