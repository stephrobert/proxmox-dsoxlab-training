# Restore ZFS mirror redundancy

**Level:** N2 · **Environment:** stockage · **Estimated time:** not calibrated

## Mission

Keep a service running on a degraded lab mirror and return the pool to healthy redundancy.

## Scope and safety

This lab targets only `Dedicated disposable two-device ZFS pool labmirror-n2-214 and evaluator-owned corpus; setup does not create or degrade a pool.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

Requires the dedicated disposable two-device `labmirror-n2-214` mirror; setup never creates or degrades a pool.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-restaurer-redondance-zfs/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only this lab’s declared fixture or manifest directory, never external resources or the cluster.
