# Scenario: Delegate pool access without widening scope

## Starting state

- Two pools and two VM sentinels
- Three test accounts
- A matrix of allowed and denied operations
- Assigned resources: VMIDs 201/n2-delegueracc and 216/n2-voisin; pools lab-n2-deleguer/lab-n2-voisin; accounts equipe-n2@pve, auditeur-n2@pve, secours-n2@pve. No disks, guest IPs, or physical NICs are assigned.

## Mission

Delegate operation of one resource pool to a team while preserving a verifiable boundary around its neighbour.

Create the two pools and two VM sentinels, then assign a least-privilege role to `equipe-n2@pve` on the assigned pool only. Keep the neighbour and node administration outside that ACL. Prove the allow/deny matrix by querying actual PVE permissions as the delegated principal; do not treat root-side ACL text as proof of effective access.

## Acceptance criteria

- **positif** — The operator performs allowed operations on the assigned pool.
  - Verify by: Perform read, start, and stop operations as the delegated identity, then inspect final task results.
- **negatif** — The same operations fail outside the assigned scope.
  - Verify by: Test a neighbouring VM, console, storage, and node administration as the delegated user—not as the evaluator.
- **priorites** — ACL evaluation and precedence are explained and reproduced.
  - Verify by: Vary group membership, a more-specific ACL, and propagation in the bounded fixture; compare predicted and actual responses.
- **revocation** — Revoking an assignment actually removes access.
  - Verify by: Remove the assigned membership, retry with the still-known identity, and inspect for orphaned ACLs.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
