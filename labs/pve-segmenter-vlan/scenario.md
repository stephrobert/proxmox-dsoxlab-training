# Scenario: Segment and diagnose VLANs

## Starting state

- Two VLANs in a closed lab
- A fixture router
- Clients and a service with identified ports
- Assigned resources: VMID 205; isolated bridge vmbr205 and VLAN IDs 285/286; no physical uplink is assigned.

## Mission

Build two segments and permit one explicit routed exception without exposing management.

Create isolated VLAN segments 285 and 286 on the named lab bridge, assign the test NICs to their intended tags, and implement only the requested inter-VLAN route. Keep management on its original path. Correct the deliberately wrong guest tag, then verify the effective PVE NIC/bridge configuration and connectivity matrix. Do not edit the physical uplink or restart host networking.

## Acceptance criteria

- **l2** — Frames remain on the intended VLAN.
  - Verify by: Compare `bridge vlan show` and captures at the designated points; verify same-VLAN communication.
- **routage** — Only the requested inter-VLAN flow passes.
  - Verify by: Test an allowed and a denied port on the same service without removing the route.
- **management** — Guest networks cannot access management.
  - Verify by: Probe administration services from each segment while preserving the admin workstation path.
- **diagnostic** — A tag error is located and corrected.
  - Verify by: Inject an unauthorized tag and capture traffic before correction; then verify the complete matrix.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
