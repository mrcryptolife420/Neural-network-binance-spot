# Data Pipeline Lineage Evidence

Roadmap: 096

`data_pipeline_evidence.py` exports local lineage:

raw -> candles -> features -> labels -> manifest -> evaluation -> model

Evidence includes data quality summary and no-live proof. Payloads are redacted before writing.
