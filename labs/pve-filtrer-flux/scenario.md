# Scenario: Filter management and guest traffic

## Starting state

- A node with an identified firewall backend
- Three independent test locations
- Known witness services listening before filtering
- Assigned resources: VMID 203 and its per-VM firewall file /etc/pve/firewall/203.fw; no physical NIC or external network is assigned.

## Mission

Apply a minimal traffic policy between administration, guests, and an unauthorized client.

Enable the PVE firewall on the assigned VM and write an explicit allow-list for the required management and guest flows. Leave default inbound policy at DROP and retain the independent console path. Keep a test service listening while checking both permitted and denied source locations. Validate the effective firewall status, not merely a local draft file.

## Acceptance criteria

- **autorise** — Required flows remain functional.
  - Verify by: Test the API, intended console, and service from authorized origins and require a real application response.
- **interdit** — Other origins are blocked by policy.
  - Verify by: Keep the service listening and probe from the denied client over IPv4 and IPv6 when enabled.
- **activation** — Rules are applied at the correct levels.
  - Verify by: Inspect backend state and matching counters/logs; a rules file alone is insufficient.
- **persistance** — Filtering and recovery access survive a restart.
  - Verify by: Restart the lab node, repeat the traffic matrix, and verify the external console path.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
