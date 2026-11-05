# Maintain a node and prepare an upgrade

**Level:** N2 · **Environment:** maintenance · **Estimated time:** not calibrated

## Mission

Maintain a lab node using prechecks, a post-change acceptance test, and a documented recovery procedure.

## Scope and safety

This lab targets only `Disposable version-qualified PVE node, verified backups, and console; setup changes no VMID or package state.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

Requires a disposable, version-qualified PVE node and verified backups; setup never upgrades a node.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-maintenir-noeud/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only this lab’s declared fixture or manifest directory, never external resources or the cluster.
