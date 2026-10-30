# Challenge: a VM that boots from its disk, and a service that answers

You work on `pve.lab`. The manifest is in
`/opt/lab-proxmox/pve-creer-vm/manifeste.md`.

## What is expected

1. VM 150 matches the lesson's hardware contract: `q35`, OVMF with
   `efidisk0`, `host` CPU, `virtio-scsi-single`, a `virtio` card on `vmbr0`,
   at most 2 cores and 2048 MB.
2. No ISO is inserted, `scsi0` comes first in the boot order, and the VM is
   running.
3. `http://10.10.113.150:8080/` serves the manifest's witness line.
4. After a reboot of the VM, the page comes back with no intervention.

## What is proven

The tests read the VM configuration with `qm config`, query the service from
the node, which is not the guest, then reboot the VM and wait for the page to
come back. They do not read the commands you typed.
