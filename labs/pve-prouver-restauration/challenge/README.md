# Challenge: Restore a service and measure recovery objectives

Restore the assigned workload into the isolated recovery network while the original data volumes are unavailable. Validate the application against the evaluator-owned write journal and record the newest acknowledged record as RPO evidence. Measure RTO from observed task timestamps through application readiness, not from a typed estimate. Confirm the original production VM and all neighbouring resources remain unchanged. If PBS/recovery fixtures are missing, stop and report the missing prerequisite.

The assigned object is `Empty recovery VMID 209 reserved for a restored VM named n2-restored-209; PBS storage lab-pbs-n2-209, evaluator-owned backup/journal, and isolated recovery network.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
