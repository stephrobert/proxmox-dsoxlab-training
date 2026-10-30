# A VM to deliver, and a service that must answer

The Proxmox node is ready. A team asks you for a virtual machine to host a
small web service, and it has already reserved its resources: the lab
manifest, in `/opt/lab-proxmox/pve-creer-vm/manifeste.md`, gives the VMID,
the storage, the ISO, the bridge and the VM address.

The team will not settle for a VM that runs. It wants a machine that **boots
from its own disk**, no longer depending on the installation ISO, and a
service it can reach **from its own workstation**, not only from the VM
console.

## Mission

1. Create VM 150 with the lesson's hardware contract: `q35` machine type, OVMF
   firmware with its EFI disk, `host` CPU, `VirtIO SCSI single` controller,
   `VirtIO` network card on `vmbr0`, at most 2 cores and 2048 MB of RAM. Its
   disks go on the `local` storage: this node has no `local-lvm`.
2. Install Debian from the provided ISO, with the static address from the
   manifest.
3. Once the installation is done, remove the ISO and make the VM boot from its
   disk.
4. In the VM, start the witness page described by the manifest, on port 8080,
   and make it come back when the machine restarts.

## What is graded

| # | What is checked | How |
|---|---|---|
| 1 | The hardware contract | the VM configuration, read by `qm config` |
| 2 | Booting from disk | no ISO inserted, `scsi0` first in the boot order, VM running |
| 3 | The service | the page read from the node contains the manifest's witness line |
| 4 | Surviving a reboot | the VM is rebooted, and the page comes back on its own |

The lab does not look at how you installed Debian: only the resulting state
counts.

## Starting over

`dsoxlab clean pve-creer-vm` destroys VM 150 and its disks. The node and the
ISO stay in place.
