# Resize a VM and prove a local rollback

The application VM is running with 1 vCPU, 1024 MiB RAM and a 4 GiB system disk. Preserve a local return point before allocating 2 vCPUs, 2048 MiB RAM and an 8 GiB disk. Extend the partition and filesystem inside Debian as well. The original witness, guest agent and static network are supplied.

Read the resource manifest on the Proxmox node at `/opt/lab-proxmox/pve-gerer-cycle-vie/manifeste.md` with administrator privileges. It lists the image, exact witness lines and, when applicable, SSH key paths. The supplied service or vendor snippet produces the witness; no service script must be written.

## What is graded

- Configure VM 195 with 2048 MiB RAM.
- Configure VM 195 with two vCPUs.
- Configure VM 195 with automatic startup enabled.
- Configure VM 195 with startup order 20.
- Run VM 195 with 2048 MiB RAM actually allocated by QEMU.
- Run VM 195 with two vCPUs actually allocated by QEMU.
- Set the PVE scsi0 disk size to 8 GiB.
- Make the guest see an 8 GiB /dev/sda disk.
- Expand the guest root filesystem to at least 7 GiB.
- Keep the guest root filesystem writable; the evaluator writes and removes an 8 MiB probe.
- Create avant-changement while the VM still has 1024 MiB RAM.
- Create avant-changement while the VM still has one vCPU.
- Include the original 4 GiB disk in avant-changement.
- Make avant-changement restore the initial nonce in /srv/temoin/retour.txt.
- Keep VM 195 serving its exact manifest witness line on 10.10.113.195:8080.
- Keep the witness service available after a clean shutdown and start of VM 195.

The evaluator writes and removes a bounded probe, temporarily rolls the VM back, then restores its entire current state using a temporary snapshot. It also performs a clean guest restart. Startup order is checked as PVE configuration; no host reboot is claimed. A local snapshot does not protect against losing its disk.
