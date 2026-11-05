# Challenge: Migrate a VMware workload with a cutover plan

Import an authorized VMware export to the isolated lab network, inventory all imported disks and dependencies, validate the running guest beyond boot, then cut over only after the source is powered off. Verify source state through the VMware API and preserve a rollback point for writes.

## What the tests observe

- The imported PVE VM has all declared disks, boots and reports a live guest-agent network interface.
- The source VMware VM is actually powered off at cutover; no duplicate active workload exists.
- A rollback snapshot/export is present before any post-cutover writes are accepted.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
