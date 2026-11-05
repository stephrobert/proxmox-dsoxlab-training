# pve-operer-ansible

Avec l’identité de lecture, démontrez qu’une opération d’alimentation est refusée, puis utilisez une identité opérateur limitée à la VM cible pour l’arrêter. Rejouez une seconde fois le playbook d’état voulu. Les tests inspectent l’état réel des VM et l’historique des tâches Proxmox, pas le texte du playbook ni un récapitulatif déclaré.

**Prérequis / conditions de blocage :** Crée deux VM de 512 Mio ; démarre la cible 1741 et la sentinelle 1742. Créez des jetons lecture et opérateur distincts, limités à ces chemins VM ; le setup n’affiche ni n’installe d’identifiants.

```bash
dsoxlab run pve-operer-ansible
dsoxlab check pve-operer-ansible
dsoxlab clean pve-operer-ansible
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
