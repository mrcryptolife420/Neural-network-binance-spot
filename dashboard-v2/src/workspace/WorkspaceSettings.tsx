export function WorkspaceSettings() {
  return (
    <section className="panel">
      <h2>Workspace Settings</h2>
      <label>
        <input type="checkbox" checked readOnly /> Safety widgets locked
      </label>
      <label>
        <input type="checkbox" checked readOnly /> Local-only storage
      </label>
    </section>
  );
}
