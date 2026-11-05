# Maintain the cluster

Perform approved node maintenance, preserve the service contract and return to
a healthy cluster. Target `proxmox-cluster`: `pve01.lab`, roles `node2=pve02.lab`,
`node3=pve03.lab`; independent local controller/probe.

```bash
dsoxlab run pve-maintenir-cluster
dsoxlab check pve-maintenir-cluster
dsoxlab clean pve-maintenir-cluster
```

[Scenario](scenario.md), [challenge](challenge/README.md).
Setup requires prepared stable nodes, checked backups and approved change;
explicit failures, no provisioning/skipping. Only local syntax checks, no
maintenance execution/attestation; duration uncalibrated. Cleanup preserves backups/guests.
