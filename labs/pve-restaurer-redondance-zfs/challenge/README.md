# Challenge: Restore ZFS mirror redundancy

Use only the named two-device disposable mirror. Identify the failed member from live ZFS state, confirm the service data stays readable while the mirror is degraded, replace only the assigned virtual device, and wait for resilver completion. Verify the pool is ONLINE, the mirror has two healthy members, and no data errors remain. State clearly that replacing a virtual device does not simulate physical-disk failure. If the dedicated mirror fixture is absent, stop; never create or degrade a pool on a production device.

The assigned object is `Dedicated disposable two-device ZFS pool labmirror-n2-214 and evaluator-owned corpus; setup does not create or degrade a pool.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
