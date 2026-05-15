export function GuidedChecklist({ items }: { items: string[] }) {
  return <ul className="checklist">{items.map((item) => <li key={item}>{item}</li>)}</ul>;
}
