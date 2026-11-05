# Challenge: Provision with Terraform and measured permissions

Adopt the prepared VM in an explicit Terraform project using the pinned bpg provider and a least-privilege API identity. Save a real plan and state. Re-plan after applying only the intended configuration; prove the actual VM configuration matches and the saved second plan is a no-op.

## What the tests observe

- Terraform state contains the exact prepared VMID, not a similarly named resource.
- The saved plan contains no delete or replacement action for that VM.
- The live Proxmox VM configuration agrees with the declared cores, memory and bridge; the saved final plan is empty.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
