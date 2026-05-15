import { useEffect, useState } from "react";
import { getJson } from "../api/client";

type Watchlist = { watchlist_id: string; name: string; symbols: string[] };

export function WatchlistsPage() {
  const [watchlists, setWatchlists] = useState<Watchlist[]>([]);
  useEffect(() => {
    getJson<{ watchlists: Watchlist[] }>("/api/watchlists").then((payload) => setWatchlists(payload.watchlists)).catch(() => undefined);
  }, []);
  return (
    <section className="panel">
      <h2>Watchlists</h2>
      {watchlists.length === 0 ? <p>No local watchlists yet.</p> : watchlists.map((item) => (
        <div key={item.watchlist_id} className="watchlist-row">
          <strong>{item.name}</strong>
          <span>{item.symbols.join(", ")}</span>
        </div>
      ))}
    </section>
  );
}
