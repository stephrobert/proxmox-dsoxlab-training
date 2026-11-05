# Filter management and guest traffic

**Level:** N2 · **Environment:** reseau · **Estimated time:** not calibrated

## Mission

Apply a minimal traffic policy between administration, guests, and an unauthorized client.

## Scope and safety

This lab targets only `VMID 203 and its per-VM firewall file /etc/pve/firewall/203.fw; no physical NIC or external network is assigned.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

The PVE node must already be installed and reachable; setup only prepares the bounded lab fixture.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-filtrer-flux/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only this lab’s declared fixture or manifest directory, never external resources or the cluster.
