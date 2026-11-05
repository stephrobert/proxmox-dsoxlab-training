# pve-installer-noeud

Installer réellement un nœud depuis une ISO contrôlée et le remettre à un collègue avec un accès vérifié.

Lisez [`scenario.fr.md`](./scenario.fr.md) avant de commencer.

```bash
dsoxlab run pve-installer-noeud
dsoxlab challenge pve-installer-noeud
dsoxlab check pve-installer-noeud
```

N'utilisez que les ressources nommées dans le manifeste. Les nœuds cluster ne sont jamais provisionnés implicitement. La réussite automatisée n'atteste pas les critères qui nécessitent une observation humaine.

Le setup exige `pve_installer_iso_volid` et `pve_installer_iso_sha256`, contrôle l'empreinte de l'ISO, puis démarre la VM attribuée 190 (2 vCPU, 4 Gio, disque 32 Gio). L'installation de Proxmox reste manuelle dans sa console.
