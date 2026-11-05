# pve-epreuve-automatisation

Complete the N4 practical assessment end to end. Use the Proxmox API for a real operation; import/manage the assigned VM with Terraform and retain a real final plan/state; build a refreshed inventory from live cluster data; operate the assigned guest with Ansible; and deliver the service and a restorable backup. Run the recipe twice without recreating or restarting the guest.

**Prerequisites / blocked conditions:** Blocked until an approved Debian cloud-init template with QEMU guest agent is available. This lab creates no PVE installation, template, or cluster.

```bash
dsoxlab run pve-epreuve-automatisation
dsoxlab check pve-epreuve-automatisation
dsoxlab clean pve-epreuve-automatisation
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
