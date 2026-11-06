# Build a cloud-init template and independent clones

The preparation provides a Debian 13 cloud image with its published SHA-512, a vendor snippet that installs the witness service, and two separate SSH client keys. It creates no template or clone. Use VM 197 for the template and VMs 198 and 199 for the clones. Keep one vCPU and 768 MiB RAM per clone, gateway and DNS 10.10.113.1, and bridge vmbr0. These bounds preserve room for the evaluator’s probe.

Read [scenario.md](./scenario.md) before starting.

```bash
dsoxlab run pve-construire-template
dsoxlab challenge pve-construire-template
dsoxlab check pve-construire-template
```
