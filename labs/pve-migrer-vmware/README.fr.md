# pve-migrer-vmware

Importez un export VMware autorisé dans le réseau isolé du lab, inventorie tous les disques et dépendances, validez l’invité au-delà du démarrage, puis ne basculez qu’après l’arrêt de la source. Vérifiez l’état source par l’API VMware et préservez un point de retour pour les écritures.

**Prérequis / conditions de blocage :** BLOQUÉ sans OVA/OVF autorisé dans /opt/lab-proxmox/import/source.ova et identifiants govc protégés pour vérifier l’état source. Le setup et le nettoyage n’éteignent jamais la source.

```bash
dsoxlab run pve-migrer-vmware
dsoxlab check pve-migrer-vmware
dsoxlab clean pve-migrer-vmware
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
