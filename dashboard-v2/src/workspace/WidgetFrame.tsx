import type { DashboardV2WorkspaceWidget } from "../types/api";
import { WidgetRenderer } from "../widgets/WidgetLibrary";

export function WidgetFrame({ widget }: { widget: DashboardV2WorkspaceWidget }) {
  return (
    <div className={widget.locked ? "widget-frame locked" : "widget-frame"}>
      <header>
        <span>{widget.title}</span>
        {widget.locked ? <small>locked</small> : <small>editable</small>}
      </header>
      <WidgetRenderer widget={widget} />
    </div>
  );
}
