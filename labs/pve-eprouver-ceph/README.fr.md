# pve-eprouver-ceph

Sur un lab Ceph dédié et isolé uniquement, relevez la santé initiale et le contrat de réplication, observez la perte contrôlée de l’OSD explicitement désigné pour le lab, vérifiez que le volume RBD reste disponible selon la politique dégradée annoncée, puis rétablissez cet OSD et prouvez que les PG redeviennent sains et la réplication est restaurée. Ne prétendez pas mesurer le matériel.

**Prérequis / conditions de blocage :** BLOQUÉ sans /etc/lab-proxmox/ceph-isolated et sans identifiant d’OSD jetable dédié dans /etc/lab-proxmox/pve-eprouver-ceph.yml sur un cluster isolé. Ne mettez jamais out un OSD partagé/de production.

```bash
dsoxlab start pve-eprouver-ceph --target proxmox-cluster
dsoxlab check pve-eprouver-ceph
dsoxlab clean pve-eprouver-ceph
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
