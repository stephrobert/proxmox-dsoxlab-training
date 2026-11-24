# An agent that does not answer, and a VM you do not cut off

## The situation

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

## What is graded

| # | What is checked | How |
|---|---|---|
| 1 | The agent | device enabled, `qm agent 180 ping` answers, channel present in the guest |
| 2 | The address | the agent reports `10.10.113.180`, ignoring the loopback |
| 3 | Workload integrity | no `qmstop` task (forced stop) since the lab started, and the witness page answers with the session data |

## Starting over

`dsoxlab clean pve-reparer-agent` destroys VM 180. A new `run` draws a new
fault, maybe the other one.

## Restore the guest agent, with no forced stop

You work on `pve.lab`. The manifest is in
`/opt/lab-proxmox/pve-reparer-agent/manifeste.md`.

### What is expected

1. The agent device is enabled, `qm agent 180 ping` answers, and the channel
   `/dev/virtio-ports/org.qemu.guest_agent.0` exists in the guest.
2. `qm agent 180 network-get-interfaces` reports `10.10.113.180`.
3. The VM was never force-stopped since the lab started, and the witness page
   still answers with the session data.

### What is proven

The tests query the agent from the node, read the Proxmox task log looking for
a `qmstop`, and read the witness page from the node.
