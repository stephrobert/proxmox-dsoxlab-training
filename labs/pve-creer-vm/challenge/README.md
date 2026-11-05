# pve-creer-vm

Create VM 150 and its HTTP witness service. The lab provides a Debian 13 installer as the recommended installation method; the distribution and installation method are not separately graded. The required result is listed below.

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

To check page origin, the evaluator temporarily disables the guest virtual interface, observes that the service becomes unreachable, then restores the interface. It does not change the node management interface.
