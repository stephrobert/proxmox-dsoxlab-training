# Scenario: Integrate Proxmox Backup Server

## Starting state

- A dedicated PBS VM
- A separate datastore volume
- A VM and CT containing reference data
- Assigned resources: PBS storage lab-pbs-n2-207; externally supplied PBS endpoint/datastore and VM/CT workloads; no PBS host is provisioned by this lab.

## Mission

Integrate a dedicated PBS and make verifiable backups of two workloads using limited identities.

Integrate only the PBS endpoint and datastore assigned in the manifest. Use its recorded TLS fingerprint and a dedicated least-privilege backup identity. Back up the named VM and CT, including their declared volumes, and inspect the actual PBS snapshot inventory. Confirm deduplication/reuse from PBS statistics rather than a typed claim. If no PBS endpoint/datastore is supplied, stop: this lab does not install PBS or invent another host.

## Acceptance criteria

- **serveur** — PBS is reachable with its TLS identity verified.
  - Verify by: Check service reachability, certificate name/chain, and rejection of an incorrect fingerprint from PVE.
- **droits** — The backup account stays within its PBS scope.
  - Verify by: Back up into its namespace and verify denial for an administrative operation or neighbouring namespace.
- **contenu** — Both workloads and their specified volumes are backed up.
  - Verify by: Inspect jobs and manifests, then restore a sample from each workload; snapshot count alone is insufficient.
- **incremental** — Reuse is measured and interpreted.
  - Verify by: Repeat a backup, modify one file, and inspect bytes transferred/reused without assuming a fixed ratio.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
