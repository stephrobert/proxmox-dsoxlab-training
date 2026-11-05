# Recover off-site

Recover a workload from secondary PBS and external rescue secrets while the
primary site is inaccessible. Runtime target `proxmox-cluster`: `pve01.lab`, roles
`node2=pve02.lab`, `node3=pve03.lab`; controller is the independent workstation.

```bash
dsoxlab run pve-reprendre-hors-site
dsoxlab check pve-reprendre-hors-site
dsoxlab clean pve-reprendre-hors-site
```

**Blocked prerequisites:** no secondary PBS, separate empty recovery PVE or
vault host is declared in this catalog. Setup fails explicitly; it does not
invent roles, reuse cluster nodes or provision services.
[Scenario](scenario.md), [challenge](challenge/README.md).
Only local syntax/content checks; duration uncalibrated. No off-site/HA
attestation. Cleanup never deletes PBS data, recovered guests or rescue keys.
