# pve-deployer-sdn

On the existing three-node `proxmox-cluster`, create and apply the dedicated VNet, attach the two prepared guests, prove guest-to-guest communication, migrate one guest to another configured node, and repeat the reachability test. Inspect and correct a mismatched MTU or unapplied SDN state when present.

**Prerequisites / blocked conditions:** BLOCKED without the existing, quorate three-node `proxmox-cluster`, an approved SDN zone, an isolated topology file at `/etc/lab-proxmox/pve-deployer-sdn.json` (using the cluster's actual node names), and an authorized guest template at VMID 9000. No nodes, PVE installation, license, or guest media are supplied by this lab.

```bash
dsoxlab start pve-deployer-sdn --target proxmox-cluster
dsoxlab check pve-deployer-sdn
dsoxlab clean pve-deployer-sdn
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
