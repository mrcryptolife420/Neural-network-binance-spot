export function CommandPalette({ entries }: { entries: string[] }) {
  return (
    <section className="panel command-palette">
      <h2>Command Palette</h2>
      <input aria-label="Search command palette" placeholder="Search" />
      <ul>{entries.map((entry) => <li key={entry}>{entry}</li>)}</ul>
    </section>
  );
}
