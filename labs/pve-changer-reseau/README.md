# Route, publish, and change networking safely

**Level:** N2 · **Environment:** reseau · **Estimated time:** not calibrated

## Mission

Configure outbound access and one controlled published service, then make a reversible network change.

## Scope and safety

This lab targets only `VMID 206; isolated bridge vmbr206; nftables chain N2LAB206; no physical uplink or default route is assigned.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

The PVE node must already be installed and reachable; setup only prepares the bounded lab fixture.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-changer-reseau/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only the lab-owned fixtures listed in its manifest; external storage, workloads, and cluster state are not removed.
