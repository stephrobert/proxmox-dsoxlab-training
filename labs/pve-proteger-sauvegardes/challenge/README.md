# Challenge: Encrypt, retain, and verify backups

Use the supplied PBS and offline key vault only. Configure the assigned backup job with encryption, a finite retention policy, and a recurring verification job. Restore a test backup using the recovered key, then confirm the expected data marker. Trigger verification against the supplied disposable corrupted fixture and confirm a PVE/PBS task or verification record reports failure. Never place the key or its contents on the PVE node.

The assigned object is `PBS storage lab-pbs-n2-208; supplied VM/backups, limited identity, and offline key vault.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
