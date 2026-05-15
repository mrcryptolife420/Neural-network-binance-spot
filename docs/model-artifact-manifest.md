# Model Artifact Manifest

Roadmap: 097

`model_artifact_manifest.py` writes a manifest for trained models:
- model id
- artifact path
- artifact sha256
- feature schema hash
- dataset id
- metrics
- no-live marker

The manifest is used by model evidence and promotion checks.
