# Secure human and machine identities

**Level:** N2 · **Environment:** mono · **Estimated time:** not calibrated

## Mission

Establish human and machine access with TLS trust, recovery, and a tested token rotation.

## Scope and safety

This lab targets only `PVE identity automation-n2@pve and privilege-separated token lab-n2; VMID 202 is the only assigned VM ACL scope.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

The PVE node must already be installed and reachable; setup only prepares the bounded lab fixture.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-securiser-identites/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only this lab’s declared fixture or manifest directory, never external resources or the cluster.
