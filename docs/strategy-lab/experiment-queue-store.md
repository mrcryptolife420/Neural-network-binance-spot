# Experiment Queue Store

The queue store writes local JSON payloads under:

```text
data/strategy-lab/queues/
```

The store rejects path traversal, redacts payloads, exports manifests, and can update job status.
