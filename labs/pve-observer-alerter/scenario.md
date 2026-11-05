# Scenario: Observe capacity and receive alerts

## Starting state

- A node and guest under bounded load
- A local notification receiver
- A disposable data volume
- Assigned resources: Live PVE node metrics; local receiver and bounded guest load are supplied externally; no guest or receiver is created.

## Mission

Monitor a service and its critical resources, trigger an alert, and resolve it.

Configure the PVE metrics/alert path for the assigned service and bounded disposable data volume. Set a threshold before exhaustion, configure a local notification receiver, and cause the supplied bounded load to cross the threshold. Verify a real PVE metric sample and delivery at the receiver. Resolve the condition and observe recovery while leaving the monitor enabled. Do not use a self-authored report as proof of delivery.

## Acceptance criteria

- **mesures** — Metrics describe the correct resource.
  - Verify by: Compare identity and values against an independent direct measurement, not just the dashboard.
- **detection** — The injected fault triggers a useful alert.
  - Verify by: Cross the disposable-volume threshold and measure alert timing, cause, and named resource.
- **reception** — The notification reaches its receiver.
  - Verify by: Inspect receipt at the witness service; a sender-side log is insufficient.
- **retour** — Recovery is observed and monitoring remains enabled.
  - Verify by: Fix the cause, observe healthy state, then reinject the fault to rule out disabled monitoring.

The executable tests cover only state observable from the assigned PVE target. Human procedure, evidence provenance, business correctness, and safety review remain explicit operator checks; a green test is not a lab attestation.

## Contract constraints

- Act only on IDs, networks, and disks explicitly assigned to this lab; preserve the recovery console.
- Alternative configurations are acceptable when they satisfy the constraints and produce the required observed state.
- Preserve useful observations before correction; redact secrets without hiding the names of checked resources.
- Keep TLS/SSH verification on the nominal path. Any experimental exception must be bounded and removed before acceptance.

## Boundaries and cleanup

Do not touch unassigned VMIDs, physical uplinks, cluster configuration, production storage, credentials, or disks. Preserve TLS/SSH verification. Stop if a declared external prerequisite is absent. Run `cleanup.yaml` only after preserving the evidence you need.
