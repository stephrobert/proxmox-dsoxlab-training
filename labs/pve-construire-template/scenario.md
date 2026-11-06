# Build a cloud-init template and independent clones

The preparation provides a Debian 13 cloud image with its published SHA-512, a vendor snippet that installs the witness service, and two separate SSH client keys. It creates no template or clone. Use VM 197 for the template and VMs 198 and 199 for the clones. Keep one vCPU and 768 MiB RAM per clone, gateway and DNS 10.10.113.1, and bridge vmbr0. These bounds preserve room for the evaluator’s probe.

Read the resource manifest on the Proxmox node at `/opt/lab-proxmox/pve-construire-template/manifeste.md` with administrator privileges. It lists the image, exact witness lines and, when applicable, SSH key paths. The supplied service or vendor snippet produces the witness; no service script must be written.

## What is graded

- Set VM 197 description to dsoxlab-lab=pve-construire-template.
- Set VM 198 description to dsoxlab-lab=pve-construire-template.
- Set VM 199 description to dsoxlab-lab=pve-construire-template.
- Convert VM 197 into a PVE template.
- Name template 197 debian13-cloud-v1.
- Keep template 197 stopped.
- Attach a cloud-init drive to template 197 as ide2.
- Import the verified manifest image as scsi0 without booting or modifying it before conversion.
- Attach the supplied cloud-init vendor snippet to template 197 so its clones inherit it.
- Name VM 198 clone-a.
- Assign 10.10.113.198/24 through cloud-init to clone-a.
- Configure only the supplied clone-a public key as the cloud-init key of VM 198.
- Allow the assigned clone-a key to log in to VM 198 as debian.
- Refuse the other clone key when authenticating to clone-a.
- Make the guest hostname of VM 198 equal clone-a.
- Finish cloud-init successfully in clone-a.
- Serve the exact manifest witness line for VMID 198 from 10.10.113.198:8080.
- Name VM 199 clone-b.
- Assign 10.10.113.199/24 through cloud-init to clone-b.
- Configure only the supplied clone-b public key as the cloud-init key of VM 199.
- Allow the assigned clone-b key to log in to VM 199 as debian.
- Refuse the other clone key when authenticating to clone-b.
- Make the guest hostname of VM 199 equal clone-b.
- Finish cloud-init successfully in clone-b.
- Serve the exact manifest witness line for VMID 199 from 10.10.113.199:8080.
- Give the two clones distinct MAC addresses.
- Give the two clones distinct machine-id values.
- Give the two clones distinct SSH host keys.
- Make the template recipe boot a fresh clone and start its witness service without manual guest changes.
- Configure VM 198 with 768 MiB RAM.
- Configure VM 198 with one vCPU.
- Configure VM 198 with cloud-init user debian.
- Configure VM 198 with DNS 10.10.113.1.
- Configure VM 198 with bridge vmbr0.
- Configure VM 198 with gateway 10.10.113.1.
- Configure VM 199 with 768 MiB RAM.
- Configure VM 199 with one vCPU.
- Configure VM 199 with cloud-init user debian.
- Configure VM 199 with DNS 10.10.113.1.
- Configure VM 199 with bridge vmbr0.
- Configure VM 199 with gateway 10.10.113.1.

The evaluator creates temporary full clone 196 with the clone-b profile and IP 10.10.113.196, checks its service, then removes it. Keep that VMID free. The vendor snippet is supplied by the lab, not a file to author. Private keys remain local. The original image and template disk must remain unmodified.

Compatibility measured on Proxmox VE 9.2.25 on 2026-11-06: generated cloud-init user data uses the deprecated scalar `user` field. The checker requires JSON status `done`, no failed stage, and no fatal error. Exit code 2 is accepted only for the exact documented scalar-user deprecation (deprecated in 22.2, removal planned in 27.2, replacement: the `users` list). Any other warning or error is refused. This is a platform warning, not an extra learner task.
