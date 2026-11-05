# Scenario: Manage LXC volume identity and backups

## Starting state

- An unprivileged CT and application user
- One managed volume and one bind mount containing two markers
- A supplied external backup
- Assigned resources: CTID 384; hostname lab-n2-volumes; managed volume lab-n2-volumes; bind mount /srv/lab-n2-share

## Mission

Repair access to a container data set and prove restoration of all requested volumes.

On the supplied unprivileged CT 384, correct the ID map so only the application identity can access its data. Preserve container restrictions. Make the managed volume and the bind mount explicit, including their backup scope. Rebuild the CT from the supplied backup and verify the two distinct data markers from inside the restored CT. If the assigned CT/template is absent, stop and report that prerequisite; do not create a replacement on a shared host.

## Acceptance criteria

- **identites** — The mapping permits only the intended user.
  - Verify by: Write through the service, inspect ownership on the host, and test denial for a different UID.
- **isolation** — The CT retains its security restrictions.
  - Verify by: Check unprivileged mode, features, and permissions; reject privileged mode, system mounts, or global write access.
- **perimetre** — Each backup has an explicit data scope.
  - Verify by: Compare the manifest and both restored markers; a restored root filesystem without external data is not sufficient.
- **restauration** — The service recovers its data after reconstruction.
  - Verify by: Restore the CT and supplemental backup on an isolated network, then verify both markers and their permissions.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
