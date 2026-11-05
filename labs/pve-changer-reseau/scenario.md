# Scenario: Route, publish, and change networking safely

## Starting state

- A simulated external and private network
- An independent console
- A witness service and documented recovery route
- Assigned resources: VMID 206; isolated bridge vmbr206; nftables chain N2LAB206; no physical uplink or default route is assigned.

## Mission

Configure outbound access and one controlled published service, then make a reversible network change.

Use the assigned isolated bridge and private guest network. Configure outbound translation and publish only the nominated service port in a dedicated nftables chain. Keep the management/default route unchanged. Stage the deliberate bad change and demonstrate that the independent-console rollback restores the original PVE/network state. Verify rule persistence and a single rule set after reload; never change the uplink, cluster link, or default route.

## Acceptance criteria

- **sortie** — The private client exits with the expected network identity.
  - Verify by: Observe source and destination at the external witness and inspect the applied route and translation.
- **entree** — Only the published port reaches the intended service.
  - Verify by: Check the external response and nonce, then verify an unpublished port is refused while its service remains listening.
- **retour** — A bad change is rolled back through the planned path.
  - Verify by: Inject a bad gateway only inside the lab and use the console recovery path without evaluator intervention.
- **reboot** — The policy persists without duplicate rules.
  - Verify by: Reload and reboot the node, repeat the tests, and confirm no duplicate rules accumulated.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
