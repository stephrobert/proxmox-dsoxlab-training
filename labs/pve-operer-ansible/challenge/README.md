# Challenge: Automate operations with Ansible

Use the reader identity to demonstrate that a VM power operation is denied, then use an operator identity scoped to the target VM to stop it. Run the same desired-state play a second time. Tests inspect actual VM states and Proxmox task history, not playbook text or a claimed recap.

## What the tests observe

- The target VM is stopped, while the running sentinel is unchanged.
- Proxmox records one successful stop for the target, not a new task for the idempotent repeat.
- The read-only identity remains unable to perform the power operation.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
