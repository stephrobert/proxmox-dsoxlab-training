# Integrate Proxmox Backup Server

**Level:** N2 · **Environment:** backup · **Estimated time:** not calibrated

## Mission

Integrate a dedicated PBS and make verifiable backups of two workloads using limited identities.

## Scope and safety

This lab targets only `PBS storage lab-pbs-n2-207; externally supplied PBS endpoint/datastore and VM/CT workloads; no PBS host is provisioned by this lab.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

Requires an externally prepared PBS endpoint/datastore and both assigned VM/CT workloads. This setup does not install or emulate PBS.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-integrer-pbs/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only the lab-owned fixtures listed in its manifest; external storage, workloads, and cluster state are not removed.
