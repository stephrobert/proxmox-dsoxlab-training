# Scenario: Restore ZFS mirror redundancy

## Starting state

- Two mirror disks and an authorized replacement
- An evaluator-owned checksummed corpus
- Access to ARC configuration
- Assigned resources: Dedicated two-device pool labmirror-n2-214 and evaluator-owned corpus; setup does not create, degrade or replace a pool.

## Mission

Keep a service running on a degraded lab mirror and return the pool to healthy redundancy.

Use only the named two-device disposable mirror. Identify the failed member from live ZFS state, confirm the service data stays readable while the mirror is degraded, replace only the assigned virtual device, and wait for resilver completion. Verify the pool is ONLINE, the mirror has two healthy members, and no data errors remain. State clearly that replacing a virtual device does not simulate physical-disk failure. If the dedicated mirror fixture is absent, stop; never create or degrade a pool on a production device.

## Acceptance criteria

- **identification** — The failed disk is correctly identified.
  - Verify by: Compare GUID, stable path, and external manifest before any replacement.
- **continuite** — Data remains accessible during the tolerated failure.
  - Verify by: Read the corpus through the service while one virtual disk is removed.
- **reconstruction** — Resilver completes and the pool returns to healthy redundancy.
  - Verify by: Wait for the final state and verify redundancy and checksums, not just command launch.
- **limites** — The report distinguishes a logical test from physical disk failure.
  - Verify by: State the real failure domain and simulation limits, and inspect ARC settings without assuming a value.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
