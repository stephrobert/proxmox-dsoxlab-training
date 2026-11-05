# pve-epreuve-deploiement

À partir d’un nœud vide installé par vos soins, livrer une VM et un CT Linux répondant au cahier des charges, puis restaurer les données du service dans une nouvelle instance.

Lisez [`scenario.fr.md`](./scenario.fr.md) avant de commencer.

```bash
dsoxlab run pve-epreuve-deploiement
dsoxlab challenge pve-epreuve-deploiement
dsoxlab check pve-epreuve-deploiement
```

N'utilisez que les ressources nommées dans le manifeste. Les nœuds cluster ne sont jamais provisionnés implicitement. La réussite automatisée n'atteste pas les critères qui nécessitent une observation humaine.

Le setup n'installe pas Proxmox et ne crée aucune VM/CT : il exige un nœud déjà installé, un modèle Debian 13 attribué via `pve_deployment_ct_template` et un bridge isolé via `pve_deployment_restore_bridge`. Les VMID 198/200 et le CTID 201 doivent être libres.
