import type { DashboardV2WorkspacePanel, DashboardV2WorkspaceWidget } from "../types/api";
import { WidgetFrame } from "./WidgetFrame";

export function WorkspacePanel({ panel, widget }: { panel: DashboardV2WorkspacePanel; widget?: DashboardV2WorkspaceWidget }) {
  return (
    <article className="workspace-panel" style={{ gridColumn: `span ${Math.min(panel.w, 12)}` }}>
      <h3>{panel.title}</h3>
      {widget ? <WidgetFrame widget={widget} /> : <p>Missing widget reference</p>}
    </article>
  );
}
