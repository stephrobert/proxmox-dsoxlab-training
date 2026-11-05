# Challenge: Secure human and machine identities

Configure the named automation identity, a human recovery path, and a privilege-separated API token. Grant only the assigned VM read/power scope. Rotate the token: keep the token ID, replace its secret through the supported PVE workflow, and prove the old secret is rejected without printing either secret. Keep TLS verification enabled; never disable certificate checks or place secrets in the evidence directory.

The assigned object is `PVE identity automation-n2@pve and privilege-separated token lab-n2; VMID 202 is the only assigned VM ACL scope.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
