# Diagnose an unavailable VM

**Level:** N2 · **Environment:** mono · **Estimated time:** not calibrated

## Mission

Restore an unavailable instance by identifying its cause while preserving data and protections.

## Scope and safety

This lab targets only `Pre-provisioned disposable VMID 211 named n2-diagnostique with its disk, guest agent, and firewall; the only injected fault is net0 on vmbr999.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

Requires the assigned disposable VMID 211 with a bootable disk, firewall, guest agent, and vmbr0 before setup injects its bridge fault.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-diagnostiquer-instance/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only this lab’s declared fixture or manifest directory, never external resources or the cluster.
