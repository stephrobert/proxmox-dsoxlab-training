# Défi : Construire un inventaire Ansible fiable

Construisez un inventaire dynamique depuis l’API Proxmox réelle, limité aux deux VM balisées du lab. Utilisez les vraies adresses de gestion des nœuds, traitez explicitement l’absence d’agent/IP et rafraîchissez plutôt que de conserver un cache périmé. Le test invoque la source d’inventaire et la compare aux ressources du cluster.

## Ce que les tests observent

- L’ensemble calculé contient exactement les deux VM balisées du lab.
- Chaque hôte pointe vers son nœud réel et son réseau de gestion ; aucune donnée agent/IP manquante n’est inventée.
- L’inventaire sans cache reflète l’état actuel du cluster.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
