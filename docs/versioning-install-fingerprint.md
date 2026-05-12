# Versioning And Install Fingerprint

`build_install_fingerprint` writes `data/releases/current-install-fingerprint.json`.

It uses `pyproject.toml`, package metadata fallback, git fallback, Python version, platform, data directory hash, and local schema versions.

