# pve-fiabiliser-inventaire

Construisez un inventaire dynamique depuis l’API Proxmox réelle, limité aux deux VM balisées du lab. Utilisez les vraies adresses de gestion des nœuds, traitez explicitement l’absence d’agent/IP et rafraîchissez plutôt que de conserver un cache périmé. Le test invoque la source d’inventaire et la compare aux ressources du cluster.

**Prérequis / conditions de blocage :** Crée deux petites VM arrêtées avec une balise propre au lab. Nécessite ansible-inventory et un identifiant API Proxmox à privilèges minimaux ; le setup n’installe pas Ansible.

```bash
dsoxlab run pve-fiabiliser-inventaire
dsoxlab check pve-fiabiliser-inventaire
dsoxlab clean pve-fiabiliser-inventaire
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
