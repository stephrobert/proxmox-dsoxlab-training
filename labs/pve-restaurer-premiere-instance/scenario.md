# Back up and restore a first VM on an isolated network

Source VM 198 already serves a session-specific witness on 10.10.113.198:8080. The preparation supplies isolated bridge vmbr9 and client namespace dsox-restore (10.10.113.240/24). Back up to /var/lib/vz/dump/pve-restaurer-premiere-instance and restore to VM 199. Keep the restored guest IP unchanged: the source and restore use different Ethernet segments. Do not connect the isolated bridge to the host network.

Read the resource manifest on the Proxmox node at `/opt/lab-proxmox/pve-restaurer-premiere-instance/manifeste.md` with administrator privileges. It lists the image, exact witness lines and, when applicable, SSH key paths. The supplied service or vendor snippet produces the witness; no service script must be written.

## What is graded

- Keep restored VM 199 without any additional network interface.
- Keep restored VM 199 description equal to dsoxlab-lab=pve-restaurer-premiere-instance.
- Keep exactly one readable, complete VMA/Zstandard backup of VM 198 in the assigned backup directory.
- Include the complete 4 GiB scsi0 system disk in the backup archive.
- Complete a successful PVE restore task to VMID 199 after lab preparation.
- Restore a distinct complete system disk with no shared backing file.
- Run restored VM 199.
- Connect restored VM 199 only through net0 on isolated bridge vmbr9.
- Give the restored VM a different MAC address from the source.
- Restore the original manifest witness line in /srv/temoin/index.html.
- Serve the restored witness over HTTP port 8080 to the isolated client dsox-restore.
- Keep the restored service working after its restart while the source VM is stopped.
- Preserve the original PVE configuration of source VM 198.
- Preserve the original witness service of source VM 198.
- Keep physical interfaces out of vmbr9.
- Keep isolated client dsox-restore unable to reach the node’s HTTPS management service on port 8006.

The evaluator reads the VMA through a checked decompression pipeline. It temporarily stops the source, restarts the restored VM, checks the service from the isolated client, then restarts the source. The source disk is not deleted. All preserved-state checks require a restored VM first.
