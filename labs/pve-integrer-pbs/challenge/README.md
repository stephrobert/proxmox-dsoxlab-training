# Challenge: Integrate Proxmox Backup Server

Integrate only the PBS endpoint and datastore assigned in the manifest. Use its recorded TLS fingerprint and a dedicated least-privilege backup identity. Back up the named VM and CT, including their declared volumes, and inspect the actual PBS snapshot inventory. Confirm deduplication/reuse from PBS statistics rather than a typed claim. If no PBS endpoint/datastore is supplied, stop: this lab does not install PBS or invent another host.

The assigned object is `PBS storage lab-pbs-n2-207; externally supplied PBS endpoint/datastore and VM/CT workloads; no PBS host is provisioned by this lab.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
