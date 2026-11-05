# Challenge: Segment and diagnose VLANs

Create isolated VLAN segments 285 and 286 on the named lab bridge, assign the test NICs to their intended tags, and implement only the requested inter-VLAN route. Keep management on its original path. Correct the deliberately wrong guest tag, then verify the effective PVE NIC/bridge configuration and connectivity matrix. Do not edit the physical uplink or restart host networking.

The assigned object is `VMID 205; isolated bridge vmbr205 and VLAN IDs 285/286; no physical uplink is assigned.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
