# Exercise HA

Measure a real imposed owner-node loss and durable service recovery without
double startup or quorum bypass. Runtime `proxmox-cluster`: `pve01.lab`, roles
`node2=pve02.lab`, `node3=pve03.lab`; independent local client/controller.

```bash
dsoxlab run pve-eprouver-ha
dsoxlab check pve-eprouver-ha
dsoxlab clean pve-eprouver-ha
```

[Scenario](scenario.md), [challenge](challenge/README.md).
Prepared three-node cluster, qualified storage/reserve, documented watchdog and
rescue controls are prerequisites, not provisioned by setup. Missing conditions
fail explicitly. Local syntax checks only; duration uncalibrated.
No HA tolerance beyond measured nested results is claimed. Cleanup preserves guests/disks.
