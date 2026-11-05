# Mission: Deliver a reproducible platform through API and IaC

Complete the N4 practical assessment end to end. Use the Proxmox API for a real operation; import/manage the assigned VM with Terraform and retain a real final plan/state; build a refreshed inventory from live cluster data; operate the assigned guest with Ansible; and deliver the service and a restorable backup. Run the recipe twice without recreating or restarting the guest.

## Acceptance criteria

1. The API UPID resolves to the actual successful task for the assigned VM.
2. Terraform state owns that exact VM and the final saved plan proposes no changes.
3. The refreshed inventory contains exactly the tagged lab guest and its live node/address.
4. Ansible leaves the intended guest state in Proxmox; the second run creates no second start/stop task.
5. The same VMID serves the challenge nonce before and after restoring its real Proxmox backup.
6. The approved template and unrelated sentinel configuration remain unchanged.

## Prerequisites

Blocked until an approved Debian cloud-init template with QEMU guest agent is available. This lab creates no PVE installation, template, or cluster.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
