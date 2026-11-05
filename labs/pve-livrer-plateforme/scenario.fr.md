# Mission : Livrer une recette reproductible et transférable

À partir d’un template Debian cloud-init préexistant et autorisé, créez la VM du lab, configurez un service HTTP avec nonce, puis rejouez le provisioning. Créez et restaurez une sauvegarde Proxmox vers une seconde VM du lab, vérifiez le même service et ne nettoyez que les ressources balisées pour ce lab.

## Critères d’acceptation

1. Le service réel répond avec le nonce du setup depuis la VM provisionnée.
2. La sauvegarde Proxmox réelle correspond à la VM et la VM restaurée sert le même nonce.
3. La sentinelle non concernée reste strictement inchangée.

## Prérequis

Bloqué tant qu’aucun template Debian cloud-init autorisé, avec agent QEMU et pont de gestion fonctionnel, n’est disponible. Le setup ne crée aucun template et n’installe aucun logiciel invité.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
