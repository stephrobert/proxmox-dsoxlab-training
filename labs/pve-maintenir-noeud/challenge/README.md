# Challenge: Maintain a node and prepare an upgrade

Use only the disposable, version-qualified node named by the manifest. Run the release-specific precheck and record its actual result before maintenance; resolve blockers or stop. Apply only the pre-approved package change, then verify node version, cluster/API health, representative workloads, and backup accessibility. The test only reads live PVE state and never upgrades the node. If the disposable node and verified backups are not supplied, do not attempt an in-place upgrade of a shared node.

The assigned object is `Disposable version-qualified PVE node, verified backups, and console; setup changes no VMID or package state.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
