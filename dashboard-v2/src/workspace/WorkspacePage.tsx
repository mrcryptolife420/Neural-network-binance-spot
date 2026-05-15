import { useEffect, useState } from "react";
import { getJson } from "../api/client";
import type { DashboardV2Workspace } from "../types/api";
import { WidgetPicker } from "./WidgetPicker";
import { WorkspaceGrid } from "./WorkspaceGrid";
import { WorkspaceSettings } from "./WorkspaceSettings";
import { WorkspaceToolbar } from "./WorkspaceToolbar";

type WidgetPayload = { widgets: { widget_type: string; title: string; category: string; locked: boolean }[] };
type WorkspaceList = { workspaces: { workspace_id: string; name: string }[] };

const fallbackWorkspace: DashboardV2Workspace = {
  workspace_id: "operator_overview",
  name: "Operator Overview",
  description: "Local fallback workspace",
  mode_scope: "all_safe_modes",
  no_live_statement: "LOCAL REALTIME DASHBOARD - NO LIVE TRADING",
  live_trading_enabled: false,
  layout: {
    widgets: [
      { widget_id: "no_live_1", widget_type: "no_live_banner", title: "No Live Banner", locked: true, settings: {} },
      { widget_id: "stop_1", widget_type: "stop_button", title: "Stop Button", locked: true, settings: {} },
      { widget_id: "runtime_1", widget_type: "runtime_status", title: "Runtime Status", locked: false, settings: {} },
      { widget_id: "chart_1", widget_type: "candle_chart", title: "Candle Chart", locked: false, settings: {} },
    ],
    panels: [
      { panel_id: "p1", title: "No Live", x: 0, y: 0, w: 12, h: 2, widget_id: "no_live_1", pinned: true, collapsed: false, query_scope: "no_live_proof" },
      { panel_id: "p2", title: "Stop", x: 0, y: 2, w: 4, h: 2, widget_id: "stop_1", pinned: true, collapsed: false, query_scope: "runtime_controls" },
      { panel_id: "p3", title: "Runtime", x: 4, y: 2, w: 4, h: 3, widget_id: "runtime_1", pinned: false, collapsed: false, query_scope: "runtime_snapshot" },
      { panel_id: "p4", title: "Market", x: 0, y: 5, w: 8, h: 4, widget_id: "chart_1", pinned: false, collapsed: false, query_scope: "candles" },
    ],
  },
};

export function WorkspacePage() {
  const [workspace, setWorkspace] = useState<DashboardV2Workspace>(fallbackWorkspace);
  const [widgets, setWidgets] = useState<WidgetPayload["widgets"]>([]);
  const [workspaces, setWorkspaces] = useState<WorkspaceList["workspaces"]>([]);

  useEffect(() => {
    getJson<WidgetPayload>("/api/widgets").then((payload) => setWidgets(payload.widgets)).catch(() => undefined);
    getJson<WorkspaceList>("/api/workspaces").then((payload) => setWorkspaces(payload.workspaces)).catch(() => undefined);
  }, []);

  return (
    <>
      <section className="panel">
        <p className="safety">{workspace.no_live_statement}</p>
        <WorkspaceToolbar name={workspace.name} />
        <p>{workspace.description}</p>
        <select value={workspace.workspace_id} onChange={() => setWorkspace(fallbackWorkspace)}>
          <option value={workspace.workspace_id}>{workspace.name}</option>
          {workspaces.map((item) => (
            <option key={item.workspace_id} value={item.workspace_id}>{item.name}</option>
          ))}
        </select>
      </section>
      <WorkspaceGrid workspace={workspace} />
      <WidgetPicker widgets={widgets} />
      <WorkspaceSettings />
    </>
  );
}
