# Challenge: plug a VM into the right bridge

You work on `pve.lab`. The manifest is in
`/opt/lab-proxmox/pve-raccorder-instance/manifeste.md`.

## What is expected

1. The `net0` card of VM 160 is on `vmbr0`, and `tap160i0` is an actual port
   of that bridge.
2. `http://10.10.113.160:8080/` serves the session's witness line.
3. The isolated bridge `vmbr9` received no physical port, and the VM was not
   recreated.
4. After a reboot of the VM and an `ifreload -a` on the node, the page comes
   back.

## What is proven

The tests read the VM configuration and the actual ports of the bridges,
query the service from the node, then reboot the guest and reload the node
network before querying it again.
