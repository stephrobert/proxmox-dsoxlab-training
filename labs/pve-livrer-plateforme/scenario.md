# Mission: Deliver a reproducible, transferable platform

Use a pre-existing, approved Debian cloud-init template to create the lab VM, configure a nonce-backed HTTP service, and run a second provisioning pass. Create and restore a Proxmox backup to a second lab VM, verify the same service, and clean only resources tagged for this lab.

## Acceptance criteria

1. The live service answers with the setup nonce from the provisioned VM.
2. The backup is a real Proxmox backup for the exact VM and the restored VM serves the same nonce.
3. The untouched sentinel remains byte-for-byte unchanged.

## Prerequisites

Blocked until an approved Debian cloud-init template with QEMU guest agent and a working management bridge is available. Setup creates no template and installs no guest software.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
