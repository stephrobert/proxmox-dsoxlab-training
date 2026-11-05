# Mission: Automate operations with Ansible

Use the reader identity to demonstrate that a VM power operation is denied, then use an operator identity scoped to the target VM to stop it. Run the same desired-state play a second time. Tests inspect actual VM states and Proxmox task history, not playbook text or a claimed recap.

## Acceptance criteria

1. The target VM is stopped, while the running sentinel is unchanged.
2. Proxmox records one successful stop for the target, not a new task for the idempotent repeat.
3. The read-only identity remains unable to perform the power operation.

## Prerequisites

Creates two 512 MiB VMs; starts target 1741 and sentinel 1742. Create separate read and operator tokens scoped to these VM paths; no credentials are printed or installed by setup.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
