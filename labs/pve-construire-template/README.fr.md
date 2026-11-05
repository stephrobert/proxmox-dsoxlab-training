# pve-construire-template

Produire un template versionné et deux clones distincts utilisables sans configuration manuelle après démarrage.

Lisez [`scenario.fr.md`](./scenario.fr.md) avant de commencer.

```bash
dsoxlab run pve-construire-template
dsoxlab challenge pve-construire-template
dsoxlab check pve-construire-template
```

N'utilisez que les ressources nommées dans le manifeste. Les nœuds cluster ne sont jamais provisionnés implicitement. La réussite automatisée n'atteste pas les critères qui nécessitent une observation humaine.

Le setup réserve les VMID 197 à 199, vérifie l'image Debian 13 et génère deux clés Ed25519 distinctes sous `/opt/lab-proxmox/pve-construire-template/keys`. Les clés privées restent sur le nœud et ne doivent pas apparaître dans les preuves.
