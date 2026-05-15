import type { DashboardV2WorkspaceWidget } from "../types/api";

export function GenericWidget({ widget }: { widget: DashboardV2WorkspaceWidget }) {
  return (
    <div className="widget-body">
      <strong>{widget.title}</strong>
      <span>{widget.widget_type}</span>
      {widget.locked ? <small>Locked safety control</small> : <small>Local analytics widget</small>}
    </div>
  );
}

export function NoLiveBannerWidget() {
  return <div className="safety">LOCAL REALTIME DASHBOARD - NO LIVE TRADING</div>;
}

export function StopButtonWidget() {
  return <button className="stop-button" type="button">Stop local bot</button>;
}

export function WidgetRenderer({ widget }: { widget: DashboardV2WorkspaceWidget }) {
  if (widget.widget_type === "no_live_banner") return <NoLiveBannerWidget />;
  if (widget.widget_type === "stop_button") return <StopButtonWidget />;
  return <GenericWidget widget={widget} />;
}
