import type { DashboardState } from "../store/dashboardStore";

export function LogsPage({ state }: { state: DashboardState }) {
  return (
    <section className="panel">
      <h2>System Logs</h2>
      <dl className="metrics">
        <div><dt>Backend</dt><dd>{state.runtime.status}</dd></div>
        <div><dt>WebSocket</dt><dd>{state.connected ? "connected" : "offline"}</dd></div>
        <div><dt>Missed events</dt><dd>{state.missedEvents}</dd></div>
        <div><dt>Render count</dt><dd>{state.renderStats.count}</dd></div>
      </dl>
      <h3>Recent events</h3>
      <ul className="event-list">
        {state.events.slice(-20).map((event, index) => <li key={`${event.topic}-${index}`}>{event.topic}</li>)}
      </ul>
    </section>
  );
}
