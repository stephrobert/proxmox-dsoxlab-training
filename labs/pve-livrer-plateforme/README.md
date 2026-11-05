# pve-livrer-plateforme

Use a pre-existing, approved Debian cloud-init template to create the lab VM, configure a nonce-backed HTTP service, and run a second provisioning pass. Create and restore a Proxmox backup to a second lab VM, verify the same service, and clean only resources tagged for this lab.

**Prerequisites / blocked conditions:** Blocked until an approved Debian cloud-init template with QEMU guest agent and a working management bridge is available. Setup creates no template and installs no guest software.

```bash
dsoxlab run pve-livrer-plateforme
dsoxlab check pve-livrer-plateforme
dsoxlab clean pve-livrer-plateforme
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
