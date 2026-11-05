# Availability assessment

Operate a three-node cluster with reserve, measure imposed service failure and
perform independent backup recovery. Runtime `proxmox-cluster`: `pve01.lab`,
`node2=pve02.lab`, `node3=pve03.lab`; external workstation controller/client.

```bash
dsoxlab run pve-epreuve-disponibilite
dsoxlab check pve-epreuve-disponibilite
dsoxlab clean pve-epreuve-disponibilite
```

**Blocked:** catalog lacks independent primary/secondary PBS, empty recovery
target and vault. Setup fails explicitly, never invents roles or provisions.
[Scenario](scenario.md), [assessment instructions](challenge/README.md).
No hints/solution during assessment; authorized documentation agreed beforehand.
Local syntax checks only, duration uncalibrated, no HA/off-site attestation.
Cleanup preserves all instructor data/resources.
