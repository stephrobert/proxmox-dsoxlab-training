# Manage LXC volume identity and backups

**Level:** N2 · **Environment:** backup · **Estimated time:** not calibrated

## Mission

Repair access to a container data set and prove restoration of all requested volumes.

## Scope and safety

This lab targets only `Pre-provisioned disposable CTID 384 named lab-n2-volumes; managed volume lab-n2-volumes; bind mount /srv/lab-n2-share.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

Requires the pre-provisioned disposable unprivileged CT 384, its supplied managed volume, bind mount, and backup.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-maitriser-volumes-lxc/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only this lab’s declared fixture or manifest directory, never external resources or the cluster.
