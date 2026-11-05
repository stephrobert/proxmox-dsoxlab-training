# Challenge: Route, publish, and change networking safely

Use the assigned isolated bridge and private guest network. Configure outbound translation and publish only the nominated service port in a dedicated nftables chain. Keep the management/default route unchanged. Stage the deliberate bad change and demonstrate that the independent-console rollback restores the original PVE/network state. Verify rule persistence and a single rule set after reload; never change the uplink, cluster link, or default route.

The assigned object is `VMID 206; isolated bridge vmbr206; nftables chain N2LAB206; no physical uplink or default route is assigned.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
