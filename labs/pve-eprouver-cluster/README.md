# Build and exercise a three-node cluster

**The learner forms the cluster.** Selecting `proxmox-cluster` makes the KVM
backend provision three Debian 13 VMs: `pve01.lab`, `pve02.lab` and `pve03.lab`
(8 GiB RAM, 4 vCPU, 40+40 GiB disks each). This lab does not run `pvecm` or
join nodes automatically. Install and verify compatible Proxmox VE on each
node, configure the isolated Corosync network, and prepare the instructor
allocation first. The local workstation is the independent controller, never
a cluster node.

```bash
dsoxlab start pve-eprouver-cluster --target proxmox-cluster
dsoxlab check pve-eprouver-cluster
dsoxlab clean pve-eprouver-cluster
```

Before `run`, supply the instructor allocation described in
[challenge/README.md](challenge/README.md). Missing nodes, PVE, verified SSH
inventory or console are explicit precondition errors, not skips.
Read [scenario.md](scenario.md). Duration is uncalibrated; no execution or HA
certification is claimed.

Cleanup restores this controller's armed actions and removes its evidence;
it never dismantles the cluster or destroys instructor guests, disks or backups.
