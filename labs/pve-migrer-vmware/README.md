# pve-migrer-vmware

Import an authorized VMware export to the isolated lab network, inventory all imported disks and dependencies, validate the running guest beyond boot, then cut over only after the source is powered off. Verify source state through the VMware API and preserve a rollback point for writes.

**Prerequisites / blocked conditions:** BLOCKED without an authorized OVA/OVF at /opt/lab-proxmox/import/source.ova and protected govc credentials for source-state verification. The source is never powered off by setup or cleanup.

```bash
dsoxlab run pve-migrer-vmware
dsoxlab check pve-migrer-vmware
dsoxlab clean pve-migrer-vmware
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
