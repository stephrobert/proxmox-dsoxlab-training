# Mission: Deploy and troubleshoot Ceph storage

On a dedicated isolated Ceph lab only, record the initial health and replica contract, observe a controlled loss of the specifically designated lab OSD, verify the RBD volume remains available under the declared degraded policy, then restore that OSD and prove PGs return clean and replication is restored. Do not claim a hardware benchmark.

## Acceptance criteria

1. The lab RBD image is readable while the designated lab OSD is degraded and the pool obeys its min_size.
2. The designated OSD returns up/in and the lab pool PGs become clean with the configured replica count.
3. Current Ceph health is queried live; no performance claim is graded.

## Prerequisites

BLOCKED unless /etc/lab-proxmox/ceph-isolated exists and /etc/lab-proxmox/pve-eprouver-ceph.yml names a dedicated disposable OSD on an isolated cluster. Never mark out a shared/production OSD.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
