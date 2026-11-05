# Migrate a VM and container

Move a VM and CT by their supported methods, preserve data and measure external
client impact. Runtime `proxmox-cluster` anchors at `pve01.lab` with
`node2=pve02.lab`, `node3=pve03.lab`; the workstation is the independent client.

```bash
dsoxlab run pve-migrer-instance
dsoxlab check pve-migrer-instance
dsoxlab clean pve-migrer-instance
```

[Scenario](scenario.md), [allocation/instructions](challenge/README.md).
Setup requires preinstalled nodes, qualified destinations and prepared VM/CT
services; it fails explicitly, never provisions or skips. Only local syntax
checks were run; no zero-interruption guarantee or PVE attestation.
Duration is uncalibrated. Cleanup never destroys guests or their disks.
