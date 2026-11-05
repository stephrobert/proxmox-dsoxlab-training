# An agent that does not answer, and a VM you do not cut off

VM 180 serves a page to a team, and its service works. But Proxmox cannot see
its address, the backup cannot freeze its file systems, and
`qm agent 180 ping` fails: the **QEMU guest agent** does not answer.

There are two possible causes, and the lab drew one at random. The manifest,
in `/opt/lab-proxmox/pve-reparer-agent/manifeste.md`, gives the VM address and
how to get into it.

## Mission

1. Find why the agent does not answer. Look at both sides: the VM
   configuration in Proxmox, and the guest itself.
2. Fix the cause. If the VM must restart, do it **cleanly**: its workload must
   close properly, as on a real server.
3. Check from the node that the agent answers and reports the VM address.

## Graded requirements

1. Restore a successful guest agent ping.
2. Enable the guest agent device in VM 180 configuration.
3. Provide /dev/virtio-ports/org.qemu.guest_agent.0 inside VM 180.
4. Have the agent report 10.10.113.180 outside the loopback interface.
5. Avoid any qmstop task for VM 180 since the lab started.
6. Keep the VM 180 witness page accessible with its exact session line.

Persistence checks perform a clean stop and start and observe both states. Unreadable measurements fail. Preservation checks only count once the report exists, the network is repaired or the agent answers, depending on the lab.

## Starting over

`dsoxlab clean pve-reparer-agent` destroys VM 180. A new `run` draws a new
fault, maybe the other one.

To check page origin, the evaluator temporarily disables the guest virtual interface, observes that the service becomes unreachable, then restores the interface. It does not change the node management interface.
