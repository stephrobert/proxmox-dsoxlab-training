# Mission: Provision with Terraform and measured permissions

Adopt the prepared VM in an explicit Terraform project using the pinned bpg provider and a least-privilege API identity. Save a real plan and state. Re-plan after applying only the intended configuration; prove the actual VM configuration matches and the saved second plan is a no-op.

## Acceptance criteria

1. Terraform state contains the exact prepared VMID, not a similarly named resource.
2. The saved plan contains no delete or replacement action for that VM.
3. The live Proxmox VM configuration agrees with the declared cores, memory and bridge; the saved final plan is empty.

## Prerequisites

Creates only stopped VM 1737. Terraform is not installed by setup. Store API credentials outside the project; protect state and plan files because they can contain sensitive values.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
