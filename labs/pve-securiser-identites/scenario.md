# Scenario: Secure human and machine identities

## Starting state

- A lab node and CA
- Limited human and machine identities
- A console path outside the filtered network
- Assigned resources: PVE identity automation-n2@pve and privilege-separated token lab-n2; VMID 202 is the only assigned VM ACL scope.

## Mission

Establish human and machine access with TLS trust, recovery, and a tested token rotation.

Configure the named automation identity, a human recovery path, and a privilege-separated API token. Grant only the assigned VM read/power scope. Rotate the token: keep the token ID, replace its secret through the supported PVE workflow, and prove the old secret is rejected without printing either secret. Keep TLS verification enabled; never disable certificate checks or place secrets in the evidence directory.

## Acceptance criteria

- **tls** — The client verifies the node identity.
  - Verify by: Succeed with the assigned CA, then present a wrong-name or wrong-chain certificate and verify rejection.
- **token** — A privilege-separated token does not inherit extra permissions.
  - Verify by: Vary only the owner permissions and verify that the token is still denied actions outside its own grants.
- **rotation** — The new token works and the old one is rejected.
  - Verify by: Perform an allowed operation before and after rotation, then replay a request with the old secret.
- **secours** — The human recovery path is documented and tested.
  - Verify by: Test MFA and the authorized recovery procedure without placing recovery codes in the report.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
