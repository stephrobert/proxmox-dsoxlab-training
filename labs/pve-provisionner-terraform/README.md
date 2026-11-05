# pve-provisionner-terraform

Adopt the prepared VM in an explicit Terraform project using the pinned bpg provider and a least-privilege API identity. Save a real plan and state. Re-plan after applying only the intended configuration; prove the actual VM configuration matches and the saved second plan is a no-op.

**Prerequisites / blocked conditions:** Creates only stopped VM 1737. Terraform is not installed by setup. Store API credentials outside the project; protect state and plan files because they can contain sensitive values.

```bash
dsoxlab run pve-provisionner-terraform
dsoxlab check pve-provisionner-terraform
dsoxlab clean pve-provisionner-terraform
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
