# Qualify shared storage

Put a dedicated NFS volume at the cluster's disposal and qualify its identity
and availability limits. Runtime `proxmox-cluster`: `pve01.lab`, roles
`node2=pve02.lab`, `node3=pve03.lab`; controller is the independent workstation.

```bash
dsoxlab run pve-qualifier-stockage-partage
dsoxlab check pve-qualifier-stockage-partage
dsoxlab clean pve-qualifier-stockage-partage
```

**Currently blocked:** the catalog has no independent NFS host. Setup explicitly
refuses this prerequisite; it does not invent a host, reuse a cluster node or
provision anything. [Scenario](scenario.md) and [challenge](challenge/README.md)
describe the complete exercise for a separately qualified source.
Only local syntax/content checks, no PVE execution; duration remains uncalibrated.
Cleanup preserves instructor guests, exports, volumes and backups.
