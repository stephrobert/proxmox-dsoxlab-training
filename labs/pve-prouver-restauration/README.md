# Restore a service and measure recovery objectives

**Level:** N2 · **Environment:** backup · **Estimated time:** not calibrated

## Mission

Recover an application from PBS with the source unavailable and produce a verifiable recovery report.

## Scope and safety

This lab targets only `Empty recovery VMID 209 reserved for a restored VM named n2-restored-209; PBS storage lab-pbs-n2-209, evaluator-owned backup/journal, and isolated recovery network.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

Requires the assigned PBS recovery fixture, evaluator-owned journal, and isolated recovery network.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-prouver-restauration/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only the lab-owned fixtures listed in its manifest; external storage, workloads, and cluster state are not removed.
