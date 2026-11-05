# Challenge: Build an SDN network for the workload

On an existing supported multi-node cluster, create and apply the dedicated VNet, attach the two prepared guests, prove guest-to-guest communication, migrate one guest to the second node, and repeat the reachability test. Correct an intentionally wrong MTU or unapplied SDN state before acceptance.

## What the tests observe

- The live VNet exists, is applied on both configured nodes, and has the intended MTU.
- Both guests have their NIC attached to that VNet and actually reach each other.
- After migration the guest is on the other node and the same peer reachability still works.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
