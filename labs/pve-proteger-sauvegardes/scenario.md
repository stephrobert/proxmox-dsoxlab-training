# Scenario: Encrypt, retain, and verify backups

## Starting state

- PBS and a limited identity
- A series of dated fixture backups
- A separate lab key vault
- Assigned resources: PBS storage lab-pbs-n2-208; supplied VM/backups, limited identity, and offline key vault.

## Mission

Configure encryption, retention, and verification, then prove a recovered key can restore data.

Use the supplied PBS and offline key vault only. Configure the assigned backup job with encryption, a finite retention policy, and a recurring verification job. Restore a test backup using the recovered key, then confirm the expected data marker. Trigger verification against the supplied disposable corrupted fixture and confirm a PVE/PBS task or verification record reports failure. Never place the key or its contents on the PVE node.

## Acceptance criteria

- **chiffrement** — The requested backup is actually encrypted.
  - Verify by: Inspect its manifest and try to read it from a client without the key; transport TLS alone does not meet this criterion.
- **cle** — The recovered key restores the correct data.
  - Verify by: Use a clean client, retrieve the recovery key, and restore the evaluator-known marker.
- **retention** — Retention preserves the expected restore points.
  - Verify by: Compare selection across fixture dates with the expected table and verify a protected point is not deleted.
- **verification** — Corruption is detected and reported.
  - Verify by: Use only the evaluator-altered disposable datastore copy; observe verify failure and notification without changing the healthy datastore.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
