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
2. Install the guest system. Debian 13 from the supplied ISO is the recommended method; the distribution and method are not graded separately. Required network and HTTP results are listed below.
3. Once the installation is done, remove the ISO and make the VM boot from its
   disk.
4. In the VM, start the witness page described by the manifest, on port 8080,
   and make it come back when the machine restarts.

## Graded requirements

1. Configure VM 150 property name as web-temoin.
2. Configure VM 150 property machine as q35.
3. Configure VM 150 property bios as ovmf.
4. Configure VM 150 property cpu as host.
5. Configure VM 150 property scsihw as virtio-scsi-single.
6. Create disk efidisk0 of VM 150 on local storage.
7. Create disk scsi0 of VM 150 on local storage.
8. Use a VirtIO model for VM 150 net0.
9. Attach VM 150 net0 to exactly vmbr0.
10. Allocate a positive amount of memory, at most 2048 MB, to VM 150.
11. Allocate a positive number of virtual CPUs, at most two, to VM 150.
12. Remove the installation ISO from VM 150.
13. Put scsi0 first in VM 150 boot order.
14. Keep VM 150 running.
15. Serve the exact session witness line at the address and port given by the manifest, reachable from the node.
16. Have the VM witness service return without intervention after a clean stop and start performed by the evaluator.

Persistence checks perform a clean stop and start and observe both states. Unreadable measurements fail. Preservation checks only count once the report exists, the network is repaired or the agent answers, depending on the lab.

## Starting over

`dsoxlab clean pve-creer-vm` destroys VM 150 and its disks. The node and the
ISO stay in place.

To check page origin, the evaluator temporarily disables the guest virtual interface, observes that the service becomes unreachable, then restores the interface. It does not change the node management interface.
