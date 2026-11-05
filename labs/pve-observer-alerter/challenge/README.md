# Challenge: Observe capacity and receive alerts

Configure the PVE metrics/alert path for the assigned service and bounded disposable data volume. Set a threshold before exhaustion, configure a local notification receiver, and cause the supplied bounded load to cross the threshold. Verify a real PVE metric sample and delivery at the receiver. Resolve the condition and observe recovery while leaving the monitor enabled. Do not use a self-authored report as proof of delivery.

The assigned object is `Live PVE node metrics; local receiver and bounded guest load are supplied externally; no guest or receiver is created.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
