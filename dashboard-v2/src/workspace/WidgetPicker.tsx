type WidgetDefinition = { widget_type: string; title: string; category: string; locked: boolean };

export function WidgetPicker({ widgets }: { widgets: WidgetDefinition[] }) {
  return (
    <aside className="widget-picker">
      <h2>Widget Library</h2>
      {widgets.slice(0, 12).map((widget) => (
        <button key={widget.widget_type} type="button" disabled={widget.locked}>
          {widget.title}
        </button>
      ))}
    </aside>
  );
}
