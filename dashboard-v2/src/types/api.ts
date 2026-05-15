export type DashboardV2Health = {
  status: string;
  app_name: string;
  supported_modes: string[];
  no_live_statement: string;
  live_trading_enabled: false;
};

export type DashboardV2Page = {
  key: string;
  title: string;
  route: string;
  live_trading_enabled: false;
};

export type DashboardV2Event = {
  event_id?: number;
  topic: string;
  payload: Record<string, unknown>;
  no_live_statement?: string;
  live_trading_enabled: false;
};

export type DashboardV2Snapshot = {
  status?: string;
  profile?: string;
  payload?: Record<string, unknown>;
  meta?: {
    payload_bytes: number;
    trimmed_counts: Record<string, number>;
    live_trading_enabled: false;
  };
  live_trading_enabled: false;
};

export type DashboardV2WorkspaceWidget = {
  widget_id: string;
  widget_type: string;
  title: string;
  locked: boolean;
  settings: Record<string, unknown>;
};

export type DashboardV2WorkspacePanel = {
  panel_id: string;
  title: string;
  x: number;
  y: number;
  w: number;
  h: number;
  widget_id: string;
  pinned: boolean;
  collapsed: boolean;
  query_scope: string;
};

export type DashboardV2Workspace = {
  workspace_id: string;
  name: string;
  description: string;
  mode_scope: string;
  layout: {
    panels: DashboardV2WorkspacePanel[];
    widgets: DashboardV2WorkspaceWidget[];
  };
  no_live_statement: string;
  live_trading_enabled: false;
};
