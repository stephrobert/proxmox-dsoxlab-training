# Challenge: Diagnose an unavailable VM

Inspect the supplied VM 211 and its PVE task/log state before changing it. The fixture injects a network-bridge fault. Identify and correct that fault without replacing the VM, deleting its disk, or weakening its firewall/agent protections. Verify the VM is running, its disk remains attached, the assigned bridge is restored, and the guest agent responds after the relevant restart.

The assigned object is `Pre-provisioned disposable VMID 211 named n2-diagnostique with its disk, guest agent, and firewall; the only injected fault is net0 on vmbr999.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes. Setup requires the actual guest fixture and refuses to synthesize a VM without its data disk.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
