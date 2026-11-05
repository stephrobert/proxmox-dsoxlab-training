# Challenge: Filter management and guest traffic

Enable the PVE firewall on the assigned VM and write an explicit allow-list for the required management and guest flows. Leave default inbound policy at DROP and retain the independent console path. Keep a test service listening while checking both permitted and denied source locations. Validate the effective firewall status, not merely a local draft file.

The assigned object is `VMID 203 and its per-VM firewall file /etc/pve/firewall/203.fw; no physical NIC or external network is assigned.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
