# Governance Evidence Bundle

Governance evidence bundles copy selected local files into a bundle directory and write a manifest with SHA-256 hash chunks and byte sizes.

The verifier recomputes hashes from the copied files and returns `ok` only when every manifest entry matches the stored file.

The bundle summary is redacted. Hash values are split into short chunks so verification is possible without creating secret-scan false positives.
