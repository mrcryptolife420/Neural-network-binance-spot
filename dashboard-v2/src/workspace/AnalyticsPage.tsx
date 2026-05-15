import { useEffect, useState } from "react";
import { getJson } from "../api/client";

export function AnalyticsPage() {
  const [payload, setPayload] = useState<Record<string, unknown>>({});
  useEffect(() => {
    getJson<Record<string, unknown>>("/api/analytics/query?scope=runtime_snapshot").then(setPayload).catch(() => undefined);
  }, []);
  return (
    <section className="panel">
      <h2>Advanced Analytics</h2>
      <pre>{JSON.stringify(payload, null, 2)}</pre>
    </section>
  );
}
