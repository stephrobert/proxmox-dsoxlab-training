# Delegate pool access without widening scope

**Level:** N2 · **Environment:** mono · **Estimated time:** not calibrated

## Mission

Delegate operation of one resource pool to a team while preserving a verifiable boundary around its neighbour.

## Scope and safety

This lab targets only `VMIDs 201/n2-delegueracc and 216/n2-voisin; pools lab-n2-deleguer and lab-n2-voisin; test accounts equipe-n2@pve, auditeur-n2@pve, and secours-n2@pve.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

The PVE node must already be installed and reachable; setup only prepares the bounded lab fixture.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-deleguer-acces/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only this lab’s declared fixture or manifest directory, never external resources or the cluster.
