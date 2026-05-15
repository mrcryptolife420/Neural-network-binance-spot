# Paper Allocation Policy

Roadmap: 099

`allocation_policy` validates local paper weights:
- total weight budget;
- per-member max weight;
- model health gate.

It returns `blocked` instead of increasing paper allocation when a member is weak.
