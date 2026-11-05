# Scenario: Maintain a node and prepare an upgrade

## Starting state

- A disposable copy of a version-qualified node
- Selected packages and a change guide
- Verified backups and a console
- Assigned resources: Disposable version-qualified node, verified backup storage and console; no VMID or package state is changed by setup.

## Mission

Maintain a lab node using prechecks, a post-change acceptance test, and a documented recovery procedure.

Use only the disposable, version-qualified node named by the manifest. Run the release-specific precheck and record its actual result before maintenance; resolve blockers or stop. Apply only the pre-approved package change, then verify node version, cluster/API health, representative workloads, and backup accessibility. The test only reads live PVE state and never upgrades the node. If the disposable node and verified backups are not supplied, do not attempt an in-place upgrade of a shared node.

## Acceptance criteria

- **precontrole** — Blocking incompatibilities are detected.
  - Verify by: Present a capacity or repository fault fixture and verify a no-go before any change begins.
- **version** — The active version matches the planned change.
  - Verify by: After reboot, inspect installed packages, booted kernel, and services—not only the package log.
- **recette** — Workloads, access, and backups work after maintenance.
  - Verify by: Repeat representative application, RBAC, and backup checks.
- **reprise** — A maintenance failure has a proven recovery path.
  - Verify by: On a dedicated clone, apply the planned rebuild/restore and verify workloads recover.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
