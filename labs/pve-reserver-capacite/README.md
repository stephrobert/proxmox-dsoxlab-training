# Reserve recovery capacity

Define placement constraints and prove an additional load cannot consume N-1
reserve. Target `proxmox-cluster`: `pve01.lab`, `node2=pve02.lab`, `node3=pve03.lab`.
The local workstation is the independent client/controller.

```bash
dsoxlab run pve-reserver-capacite
dsoxlab check pve-reserver-capacite
dsoxlab clean pve-reserver-capacite
```

[Scenario](scenario.md), [challenge](challenge/README.md).
Setup explicitly requires prepared nodes/guests and budgets; never provisions
or skips. Only local syntax checks; duration uncalibrated, no HA attestation.
Cleanup preserves cluster, guests, disks and backups.
