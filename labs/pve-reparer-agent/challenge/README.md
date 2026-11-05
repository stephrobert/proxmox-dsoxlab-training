# pve-reparer-agent

Restore the guest agent of VM 180 while preserving the supplied workload.

## Graded requirements

1. Restore a successful guest agent ping.
2. Enable the guest agent device in VM 180 configuration.
3. Provide /dev/virtio-ports/org.qemu.guest_agent.0 inside VM 180.
4. Have the agent report 10.10.113.180 outside the loopback interface.
5. Avoid any qmstop task for VM 180 since the lab started.
6. Keep the VM 180 witness page accessible with its exact session line.

Persistence checks perform a clean stop and start and observe both states. Unreadable measurements fail. Preservation checks only count once the report exists, the network is repaired or the agent answers, depending on the lab.

To check page origin, the evaluator temporarily disables the guest virtual interface, observes that the service becomes unreachable, then restores the interface. It does not change the node management interface.
