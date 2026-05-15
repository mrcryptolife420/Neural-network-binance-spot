import type { DashboardV2Event, DashboardV2Health, DashboardV2Page, DashboardV2Snapshot } from "../types/api";

export type DashboardState = {
  health?: DashboardV2Health;
  pages: DashboardV2Page[];
  connected: boolean;
  stale: boolean;
  missedEvents: number;
  lastEventId?: number;
  events: DashboardV2Event[];
  runtime: { status: string; snapshot?: DashboardV2Snapshot };
  charts: { candles: unknown[]; equity: unknown[]; paused: boolean; maxPoints: number };
  orders: { rows: unknown[]; maxRows: number };
  sessions: { rows: unknown[]; maxRows: number };
  evidence: { rows: unknown[]; maxRows: number };
  operator: { cutoverGrade?: string; noLiveProofVisible: boolean };
  settings: { profile: string; renderDebug: boolean };
  renderStats: { count: number; slowRenderWarning: boolean };
};

export const initialDashboardState: DashboardState = {
  pages: [],
  connected: false,
  stale: false,
  missedEvents: 0,
  events: [],
  runtime: { status: "idle" },
  charts: { candles: [], equity: [], paused: false, maxPoints: 500 },
  orders: { rows: [], maxRows: 250 },
  sessions: { rows: [], maxRows: 100 },
  evidence: { rows: [], maxRows: 100 },
  operator: { noLiveProofVisible: true },
  settings: { profile: "overview", renderDebug: false },
  renderStats: { count: 0, slowRenderWarning: false },
};

function tail<T>(items: T[], limit: number): T[] {
  return items.slice(Math.max(0, items.length - limit));
}

export function reduceEvent(state: DashboardState, event: DashboardV2Event): DashboardState {
  if (event.event_id !== undefined && event.event_id === state.lastEventId) {
    return { ...state, missedEvents: state.missedEvents + 1 };
  }
  const nextEvents = tail([...state.events, event], 100);
  const next: DashboardState = {
    ...state,
    connected: true,
    stale: false,
    lastEventId: event.event_id ?? state.lastEventId,
    events: nextEvents,
    renderStats: { ...state.renderStats, count: state.renderStats.count + 1 },
  };
  if (event.topic === "runtime.snapshot") {
    next.runtime = { status: "run", snapshot: event.payload as DashboardV2Snapshot };
  }
  if (event.topic === "chart.candle" && !state.charts.paused) {
    next.charts = { ...state.charts, candles: tail([...state.charts.candles, event.payload], state.charts.maxPoints) };
  }
  return next;
}

export function applySnapshot(state: DashboardState, snapshot: DashboardV2Snapshot): DashboardState {
  const payload = snapshot.payload ?? {};
  return {
    ...state,
    runtime: { status: "ready", snapshot },
    charts: {
      ...state.charts,
      candles: tail((payload.candles as unknown[]) ?? state.charts.candles, state.charts.maxPoints),
      equity: tail((payload.equity as unknown[]) ?? state.charts.equity, state.charts.maxPoints),
    },
    orders: { ...state.orders, rows: tail((payload.fills as unknown[]) ?? state.orders.rows, state.orders.maxRows) },
  };
}
