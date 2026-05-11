# Support Bundle

Support bundles collect redacted local diagnostics for debugging. Live trading remains disabled and bundles do not contain real API secrets.

Create a bundle:

```powershell
spot-bot support-bundle --json
spot-bot support-bundle --output data/support/support-bundle.zip --json
```

The bundle includes:

- `diagnostics.json`
- `preflight.json`
- `settings-redacted.json`
- selected redacted evidence artifacts
- `manifest.json` with file sizes and SHA-256 hashes

The bundle excludes `.env`, key files and raw secrets. Every payload is redacted before writing.

Verify a bundle:

```powershell
spot-bot support-bundle-verify --bundle data/support/support-bundle.zip --json
```
