# pve-eprouver-ceph

On a dedicated isolated Ceph lab only, record the initial health and replica contract, observe a controlled loss of the specifically designated lab OSD, verify the RBD volume remains available under the declared degraded policy, then restore that OSD and prove PGs return clean and replication is restored. Do not claim a hardware benchmark.

**Prerequisites / blocked conditions:** BLOCKED unless /etc/lab-proxmox/ceph-isolated exists and /etc/lab-proxmox/pve-eprouver-ceph.yml names a dedicated disposable OSD on an isolated cluster. Never mark out a shared/production OSD.

```bash
dsoxlab start pve-eprouver-ceph --target proxmox-cluster
dsoxlab check pve-eprouver-ceph
dsoxlab clean pve-eprouver-ceph
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
