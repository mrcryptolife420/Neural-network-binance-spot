import type { DashboardV2Workspace } from "../types/api";
import { WorkspacePanel } from "./WorkspacePanel";

export function WorkspaceGrid({ workspace }: { workspace: DashboardV2Workspace }) {
  const widgets = new Map(workspace.layout.widgets.map((widget) => [widget.widget_id, widget]));
  return (
    <section className="workspace-grid">
      {workspace.layout.panels.map((panel) => (
        <WorkspacePanel key={panel.panel_id} panel={panel} widget={widgets.get(panel.widget_id)} />
      ))}
    </section>
  );
}
