# Mission: Build an SDN network for the workload

On the existing three-node `proxmox-cluster`, create and apply the dedicated VNet, attach the two prepared guests, prove guest-to-guest communication, migrate one guest to another configured node, and repeat the reachability test. Inspect and correct a mismatched MTU or unapplied SDN state when present.

## Acceptance criteria

1. The live VNet exists, is applied on all three configured nodes, and has the intended MTU.
2. Both guests have their NIC attached to that VNet and actually reach each other.
3. After migration the guest is on the other node and the same peer reachability still works.

## Prerequisites

BLOCKED without the existing, quorate three-node `proxmox-cluster`, an approved SDN zone, an isolated topology file at `/etc/lab-proxmox/pve-deployer-sdn.json` using the cluster's actual node names, and an authorized guest template at VMID 9000. No nodes, PVE installation, license, or guest media are supplied by this lab.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
