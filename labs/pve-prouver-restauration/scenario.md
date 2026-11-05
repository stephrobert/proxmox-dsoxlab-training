# Scenario: Restore a service and measure recovery objectives

## Starting state

- A backup containing data and its declared dependency
- An evaluator-owned write journal
- A recovery network without production access
- Assigned resources: empty restore VMID 209 named n2-restored-209; PBS storage lab-pbs-n2-209; isolated recovery network

## Mission

Recover an application from PBS with the source unavailable and produce a verifiable recovery report.

Restore the assigned workload into the isolated recovery network while the original data volumes are unavailable. Validate the application against the evaluator-owned write journal and record the newest acknowledged record as RPO evidence. Measure RTO from observed task timestamps through application readiness, not from a typed estimate. Confirm the original production VM and all neighbouring resources remain unchanged. If PBS/recovery fixtures are missing, stop and report the missing prerequisite.

## Acceptance criteria

- **source-absente** — Recovery works without the original volumes.
  - Verify by: Remove source-volume access before restore and verify the identifiers of restored volumes.
- **donnees** — The application recovers a coherent business state.
  - Verify by: Perform application reads and writes; verify relationships and restored markers.
- **mesures** — RPO/RTO are derived from observations.
  - Verify by: Compare external probe timestamps, write sequence, and newest restored point; reject untraced typed durations.
- **isolement** — The recovery test changes no neighbouring workload.
  - Verify by: Check the isolated network, test secrets, and a sentinel’s integrity before and after the test.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
