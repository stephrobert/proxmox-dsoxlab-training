# Observe capacity and receive alerts

**Level:** N2 · **Environment:** mono · **Estimated time:** not calibrated

## Mission

Monitor a service and its critical resources, trigger an alert, and resolve it.

## Scope and safety

This lab targets only `Live PVE node metrics; local receiver and bounded guest load are supplied externally; no guest or receiver is created.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

The PVE node must already be installed and reachable; setup only prepares the bounded lab fixture.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-observer-alerter/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only this lab’s declared fixture or manifest directory, never external resources or the cluster.
