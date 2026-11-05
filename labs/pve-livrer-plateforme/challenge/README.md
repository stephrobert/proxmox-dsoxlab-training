# Challenge: Deliver a reproducible, transferable platform

Use a pre-existing, approved Debian cloud-init template to create the lab VM, configure a nonce-backed HTTP service, and run a second provisioning pass. Create and restore a Proxmox backup to a second lab VM, verify the same service, and clean only resources tagged for this lab.

## What the tests observe

- The live service answers with the setup nonce from the provisioned VM.
- The backup is a real Proxmox backup for the exact VM and the restored VM serves the same nonce.
- The untouched sentinel remains byte-for-byte unchanged.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
