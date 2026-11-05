# Challenge: Deliver a reproducible platform through API and IaC

Complete the N4 practical assessment end to end using the Proxmox API, Terraform, refreshed Ansible inventory, idempotent Ansible operations and a bounded delivery recipe.

## What the tests observe

- The API UPID resolves to the actual successful task for the assigned VM.
- Terraform state owns that exact VM and the final saved plan proposes no changes.
- The refreshed inventory contains exactly the tagged guest and its live node/address.
- Proxmox records one actual guest start; the repeat creates no second start/stop task.
- The same VM serves the challenge nonce before and after restoring its real backup.
- The approved template and unrelated sentinel configuration remain unchanged.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
