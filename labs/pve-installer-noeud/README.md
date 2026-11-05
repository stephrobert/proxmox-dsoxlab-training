# pve-installer-noeud

Installer réellement un nœud depuis une ISO contrôlée et le remettre à un collègue avec un accès vérifié.

Read [`scenario.md`](./scenario.md) before starting.

```bash
dsoxlab run pve-installer-noeud
dsoxlab challenge pve-installer-noeud
dsoxlab check pve-installer-noeud
```

Only use resources named in this lab's manifest. Cluster nodes are never provisioned implicitly. Automated success alone does not attest criteria requiring human observation.

Setup requires `pve_installer_iso_volid` and `pve_installer_iso_sha256`, verifies the ISO, and starts assigned VM 190 (2 vCPU, 4 GiB, 32 GiB disk). Proxmox installation remains a manual task in its console.
