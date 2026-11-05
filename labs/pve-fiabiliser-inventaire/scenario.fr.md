# Mission : Construire un inventaire Ansible fiable

Construisez un inventaire dynamique depuis l’API Proxmox réelle, limité aux deux VM balisées du lab. Utilisez les vraies adresses de gestion des nœuds, traitez explicitement l’absence d’agent/IP et rafraîchissez plutôt que de conserver un cache périmé. Le test invoque la source d’inventaire et la compare aux ressources du cluster.

## Critères d’acceptation

1. L’ensemble calculé contient exactement les deux VM balisées du lab.
2. Chaque hôte pointe vers son nœud réel et son réseau de gestion ; aucune donnée agent/IP manquante n’est inventée.
3. L’inventaire sans cache reflète l’état actuel du cluster.

## Prérequis

Crée deux petites VM arrêtées avec une balise propre au lab. Nécessite ansible-inventory et un identifiant API Proxmox à privilèges minimaux ; le setup n’installe pas Ansible.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
