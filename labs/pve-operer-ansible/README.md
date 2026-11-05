# pve-operer-ansible

Use the reader identity to demonstrate that a VM power operation is denied, then use an operator identity scoped to the target VM to stop it. Run the same desired-state play a second time. Tests inspect actual VM states and Proxmox task history, not playbook text or a claimed recap.

**Prerequisites / blocked conditions:** Creates two 512 MiB VMs; starts target 1741 and sentinel 1742. Create separate read and operator tokens scoped to these VM paths; no credentials are printed or installed by setup.

```bash
dsoxlab run pve-operer-ansible
dsoxlab check pve-operer-ansible
dsoxlab clean pve-operer-ansible
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
