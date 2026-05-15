# Data Store V2 Contracts

Roadmap: 096

`data_store_v2.py` adds typed local artifact contracts:
- `DataArtifactRef`
- `DataStoreManifest`
- `DataStorePathPolicy`
- `DataStoreRoot`

Each artifact gets:
- path
- artifact type
- schema version
- sha256
- row count
- no-live marker

The implementation is intentionally JSON/JSONL-first so it does not force a database or cloud feature store.
