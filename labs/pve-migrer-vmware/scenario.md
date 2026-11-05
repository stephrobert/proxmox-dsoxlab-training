# Mission: Migrate a VMware workload with a cutover plan

Import an authorized VMware export to the isolated lab network, inventory all imported disks and dependencies, validate the running guest beyond boot, then cut over only after the source is powered off. Verify source state through the VMware API and preserve a rollback point for writes.

## Acceptance criteria

1. The imported PVE VM has all declared disks, boots and reports a live guest-agent network interface.
2. The source VMware VM is actually powered off at cutover; no duplicate active workload exists.
3. A rollback snapshot/export is present before any post-cutover writes are accepted.

## Prerequisites

BLOCKED without an authorized OVA/OVF at /opt/lab-proxmox/import/source.ova and protected govc credentials for source-state verification. The source is never powered off by setup or cleanup.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
