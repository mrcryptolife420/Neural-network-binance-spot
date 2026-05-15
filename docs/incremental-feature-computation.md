# Incremental Feature Computation

Roadmap: 096

`IncrementalFeatureBuilder` stores candle state and appends only unseen feature rows after recomputing through the existing deterministic `build_feature_rows` function.

This avoids a second feature implementation while preparing the runtime to avoid full-list feature rebuilds on every step.
