# Challenge: Deploy and troubleshoot Ceph storage

On a dedicated isolated Ceph lab only, record the initial health and replica contract, observe a controlled loss of the specifically designated lab OSD, verify the RBD volume remains available under the declared degraded policy, then restore that OSD and prove PGs return clean and replication is restored. Do not claim a hardware benchmark.

## What the tests observe

- The lab RBD image is readable while the designated lab OSD is degraded and the pool obeys its min_size.
- The designated OSD returns up/in and the lab pool PGs become clean with the configured replica count.
- Current Ceph health is queried live; no performance claim is graded.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
