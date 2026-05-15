export function WorkspaceToolbar({ name }: { name: string }) {
  return (
    <div className="workspace-toolbar">
      <h2>{name}</h2>
      <button type="button">Save layout</button>
      <button type="button">Export</button>
      <button type="button">Reset safe defaults</button>
    </div>
  );
}
