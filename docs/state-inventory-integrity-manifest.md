# State Inventory Integrity Manifest

`state_inventory` walks the local data directory and records category, suffix, size, modified time, short hash, restore priority, and include eligibility.

Forbidden files are marked as not eligible and are not hashed into backup manifests.

