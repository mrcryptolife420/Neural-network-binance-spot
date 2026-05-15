import { useEffect, useState } from "react";
import { getJson } from "../api/client";

export function PreferencesPage() {
  const [preferences, setPreferences] = useState<Record<string, unknown>>({});
  useEffect(() => {
    getJson<{ preferences: Record<string, unknown> }>("/api/preferences").then((payload) => setPreferences(payload.preferences)).catch(() => undefined);
  }, []);
  return (
    <section className="panel">
      <h2>Operator Preferences</h2>
      <dl className="metrics">
        {Object.entries(preferences).slice(0, 8).map(([key, value]) => (
          <div key={key}>
            <dt>{key}</dt>
            <dd>{String(value)}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
