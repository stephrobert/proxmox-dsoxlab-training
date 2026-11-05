# pve-livrer-plateforme

À partir d’un template Debian cloud-init préexistant et autorisé, créez la VM du lab, configurez un service HTTP avec nonce, puis rejouez le provisioning. Créez et restaurez une sauvegarde Proxmox vers une seconde VM du lab, vérifiez le même service et ne nettoyez que les ressources balisées pour ce lab.

**Prérequis / conditions de blocage :** Bloqué tant qu’aucun template Debian cloud-init autorisé, avec agent QEMU et pont de gestion fonctionnel, n’est disponible. Le setup ne crée aucun template et n’installe aucun logiciel invité.

```bash
dsoxlab run pve-livrer-plateforme
dsoxlab check pve-livrer-plateforme
dsoxlab clean pve-livrer-plateforme
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
