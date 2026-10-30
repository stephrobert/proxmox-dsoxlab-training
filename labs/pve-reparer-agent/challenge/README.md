# Challenge: restore the guest agent, with no forced stop

You work on `pve.lab`. The manifest is in
`/opt/lab-proxmox/pve-reparer-agent/manifeste.md`.

## What is expected

1. The agent device is enabled, `qm agent 180 ping` answers, and the channel
   `/dev/virtio-ports/org.qemu.guest_agent.0` exists in the guest.
2. `qm agent 180 network-get-interfaces` reports `10.10.113.180`.
3. The VM was never force-stopped since the lab started, and the witness page
   still answers with the session data.

## What is proven

The tests query the agent from the node, read the Proxmox task log looking for
a `qmstop`, and read the witness page from the node.
