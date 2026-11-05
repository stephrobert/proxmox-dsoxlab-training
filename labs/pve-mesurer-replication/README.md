# Measure replication

Configure ZFS replication and establish the exact recoverable sequence.
Runtime `proxmox-cluster`: `pve01.lab`, `node2=pve02.lab`, `node3=pve03.lab`, independent
workstation controller/client. [Scenario](scenario.md), [challenge](challenge/README.md).

```bash
dsoxlab run pve-mesurer-replication
dsoxlab check pve-mesurer-replication
dsoxlab clean pve-mesurer-replication
```

Setup requires prepared PVE nodes, qualified ZFS volumes and durable journal VM;
missing prerequisites fail clearly, never provision or skip. Syntax checks only;
duration uncalibrated. Replication is neither zero-RPO nor backup/HA certification.
Cleanup preserves replicas, snapshots and guests; rollback is explicitly bounded.
