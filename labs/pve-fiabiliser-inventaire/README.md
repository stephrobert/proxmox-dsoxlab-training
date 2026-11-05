# pve-fiabiliser-inventaire

Build a dynamic inventory from the live Proxmox API for only the two tagged lab VMs. Use their actual node management addresses, explicit handling for missing agent/IP data, and refresh rather than stale cache. The test invokes the inventory source and compares it with live cluster resources.

**Prerequisites / blocked conditions:** Creates two small stopped VMs with the lab-only tag. Requires ansible-inventory and a working, least-privilege Proxmox API credential; setup does not install Ansible.

```bash
dsoxlab run pve-fiabiliser-inventaire
dsoxlab check pve-fiabiliser-inventaire
dsoxlab clean pve-fiabiliser-inventaire
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
