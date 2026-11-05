# Challenge: Manage LXC volume identity and backups

On the supplied unprivileged CT 384, correct the ID map so only the application identity can access its data. Preserve container restrictions. Make the managed volume and the bind mount explicit, including their backup scope. Rebuild the CT from the supplied backup and verify the two distinct data markers from inside the restored CT. If the assigned CT/template is absent, stop and report that prerequisite; do not create a replacement on a shared host.

The assigned object is `Pre-provisioned disposable CTID 384 named lab-n2-volumes; managed volume lab-n2-volumes; bind mount /srv/lab-n2-share.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
