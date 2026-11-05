# Segment and diagnose VLANs

**Level:** N2 · **Environment:** reseau · **Estimated time:** not calibrated

## Mission

Build two segments and permit one explicit routed exception without exposing management.

## Scope and safety

This lab targets only `VMID 205; isolated bridge vmbr205 and VLAN IDs 285/286; no physical uplink is assigned.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

The PVE node must already be installed and reachable; setup only prepares the bounded lab fixture.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-segmenter-vlan/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only the lab-owned fixtures listed in its manifest; external storage, workloads, and cluster state are not removed.
