# Scenario: Diagnose an unavailable VM

## Starting state

- An instance with one injected fault among boot, network, agent, or test volume
- Accessible logs
- Data and security sentinels
- Assigned resources: VMID 211; VM name n2-diagnostique; single injected fault: net0 bridge vmbr999

## Mission

Restore an unavailable instance by identifying its cause while preserving data and protections.

Inspect the supplied VM 211 and its PVE task/log state before changing it. The fixture injects a network-bridge fault. Identify and correct that fault without replacing the VM, deleting its disk, or weakening its firewall/agent protections. Verify the VM is running, its disk remains attached, the assigned bridge is restored, and the guest agent responds after the relevant restart.

## Acceptance criteria

- **diagnostic** — The diagnosed cause matches the injected fault.
  - Verify by: Compare timestamped observations with the evaluator-owned fault register; a written diagnosis alone is insufficient.
- **service** — The target service is actually restored.
  - Verify by: Complete a transaction and check its nonce from the external client.
- **integrite** — Data and security controls are preserved.
  - Verify by: Verify markers, firewall, and ACLs; reject destructive recreation, privileged mode, or global disablement.
- **durable** — The repair survives the relevant restart.
  - Verify by: Restart the affected component and repeat the check; do not require an unrelated host reboot.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
