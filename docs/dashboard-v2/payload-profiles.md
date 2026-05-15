# Payload Profiles

`/api/runtime/snapshot?profile=overview` returns compact operator data. `chart`, `orders`, `sessions`, `evidence`, `debug` and `full` are explicit profiles with tail limits.

The backend returns payload byte counts and trimmed counts so large candles, fills and signals do not force full dashboard refreshes.
